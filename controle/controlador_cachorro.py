from limite.tela_cachorro import TelaCachorro
from entidade.cachorro import Cachorro
from DAOs.cachorro_dao import CachorroDAO
from DAOs.vacinacao_dao import VacinacaoDAO
from entidade.porte import Porte
from entidade.vacinacao import Vacinacao
from exceptions.IdNotFound import *


class ControladorCachorro:
    def __init__(self, controlador_sistema):
        self.__cachorro_DAO = CachorroDAO()
        self.__vacinacao_DAO = VacinacaoDAO()
        self.__tela_cachorro = TelaCachorro()
        self.__controlador_sistema = controlador_sistema


    def incluir_cachorro(self, modo = "cadastrado"):
        dados_cachorro = self.__tela_cachorro.pega_dados_cachorro(modo="cadastro")
        try:
            vacinas = []
            for x in range(len(dados_cachorro["vacinas"])):
                vacina = Vacinacao(dados_cachorro["datas_vacinas"][x], dados_cachorro["vacinas"][x], dados_cachorro["id"], tipo_animal="cachorro")
                vacinas.append(vacina)

            cachorro = Cachorro(dados_cachorro["id"], dados_cachorro["nome"], dados_cachorro["raca"], dados_cachorro["porte"], vacinas)
            conferir_cachorro = self.buscar_cachorro_por_id(cachorro.id)
            if conferir_cachorro is None:
                self.__cachorro_DAO.add(cachorro)
                if vacinas:
                    self.__vacinacao_DAO.add(vacinas)
                if modo=="doado":
                    return cachorro
            else:
                self.__tela_cachorro.erro("ID já cadastrado")

        except Exception as e:
            self.__tela_cachorro.erro(f"Erro ao cadastrar cachorro: {str(e)}")


    def gerenciar_cachorros(self):
        # Cria a lista formatada de cachorros com vacinas
        if not self.__cachorro_DAO.get_all():  # Verifica se a lista de cachorros está vazia
            self.__tela_cachorro.erro("Nenhum cachorro cadastrado.")
            return

        cachorros_formatados = []
        for cachorro in self.__cachorro_DAO.get_all():
            vacinas = ", ".join([f"{v.tipo_vacina.name} (Data: {v.dia_vacina.strftime('%d/%m/%Y')})" for v in cachorro.vacinas]) if cachorro.vacinas else "Nenhuma vacina"
            cachorros_formatados.append({
                "id": cachorro.id, "nome": cachorro.nome, "raca": cachorro.raca, 
                "porte": cachorro.porte.name, "vacinas": vacinas
            })

        acao = self.__tela_cachorro.mostra_cachorro(cachorros_formatados)
        if acao:
            tipo_acao, id_cachorro = acao
            if tipo_acao == "alterar":
                self.alterar_cachorro(id_cachorro)
            elif tipo_acao == "excluir":
                self.excluir_cachorro(id_cachorro)


    def alterar_cachorro(self, id):
        cachorro = self.buscar_cachorro_por_id(id)
        if cachorro is None:
            self.__tela_cachorro.erro(idnotfound(cachorro.id))
            return 0

        # Abre a tela para editar os dados do cachorro
        cachorroeditado = self.__tela_cachorro.pega_dados_cachorro(modo="alteracao",dados_existentes=id)

        if not cachorroeditado:  # Caso a edição seja cancelada
            return 0

        try:
            # Atualiza as vacinas do cachorro
            novas_vacinas = []
            for i in range(len(cachorroeditado["vacinas"])):
                vacina_existente = next(
                    (v for v in cachorro.vacinas if v.tipo_vacina == cachorroeditado["vacinas"][i]),
                    None
                )
                if vacina_existente:
                    vacina_existente.dia_vacina = cachorroeditado["datas_vacinas"][i]
                else:
                    novas_vacinas.append(
                        Vacinacao(cachorroeditado["datas_vacinas"][i], cachorroeditado["vacinas"][i], cachorroeditado["id"], tipo_animal="cachorro")
                    )
            
            # Atualiza as informações do cachorro
            cachorro.nome = cachorroeditado["nome"]
            cachorro.raca = cachorroeditado["raca"]

            try:
                cachorro.porte = Porte(cachorroeditado["porte"])
            except ValueError:
                self.__tela_cachorro.erro("Erro: O porte informado é inválido.")
                raise ValueError("Porte inválido.")

            cachorro.vacinas = novas_vacinas

            self.__cachorro_DAO.update(cachorro)
            # Registra no histórico as novas vacinações
            if novas_vacinas:
                self.__vacinacao_DAO.update(novas_vacinas)


            return 1
        except Exception as e:
            self.__tela_cachorro.erro(f"Erro ao alterar cachorro: {str(e)}")
            return 0


    def excluir_cachorro(self, id, modo = "excluir"):
        cachorro = self.buscar_cachorro_por_id(id)

        if(cachorro is not None):
            self.__cachorro_DAO.remove(cachorro.id)
            if modo == "excluir":
                self.__vacinacao_DAO.remove((cachorro.id, "cachorro"))
        else:
            self.__tela_cachorro.erro("ATENCAO: Cachorro não existente")


    def buscar_historico_vacinacao(self):
        if self.__vacinacao_DAO.get_all():  # Verifica se a lista não está vazia
            vacinas = []
            for i in self.__vacinacao_DAO.get_all():
                for j in i:
                    if j.tipo_animal == "cachorro":
                        adotado = self.buscar_cachorro_por_id(j.id_animal)
                        if adotado is None:
                            vacinas.append(f"Status: ADOTADO, Vacina: {j.tipo_vacina.name}, Data: {j.dia_vacina}, para o {j.tipo_animal} de ID: {j.id_animal}")
                        else:
                            vacinas.append(f"Vacina: {j.tipo_vacina.name}, Data: {j.dia_vacina}, para o {j.tipo_animal} de ID: {j.id_animal}")
            self.__tela_cachorro.exibir_vacinas("\n".join(vacinas))
        else:
            self.__tela_cachorro.exibir_vacinas("Histórico de vacinas vazio.")


    def buscar_cachorro_por_id(self, id):
        try:  
            cachorro = self.__cachorro_DAO.get(id)
            return cachorro
        except idnotfound as e:
            return None 



    def retornar(self):
        self.__controlador_sistema.abre_tela()


    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_cachorro,
            2: self.gerenciar_cachorros,
            3: self.buscar_historico_vacinacao,
            0: self.retornar
        }

        while True:
            opcao = self.__tela_cachorro.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)
            funcao_escolhida()

    