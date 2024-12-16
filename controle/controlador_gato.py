from limite.tela_gato import TelaGato
from entidade.gato import Gato 
from entidade.vacinacao import Vacinacao
from DAOs.vacinacao_dao import VacinacaoDAO
from DAOs.gato_dao import GatoDAO
from exceptions.IdNotFound import *

class ControladorGato:
    def __init__(self, controlador_sistema):
        self.__gato_DAO = GatoDAO()
        self.__vacinacao_DAO = VacinacaoDAO()
        self.__tela_gato = TelaGato()
        self.__controlador_sistema = controlador_sistema


    def incluir_gato(self, modo = "cadastrado"):
        dados_gato = self.__tela_gato.pega_dados_gato(modo="cadastro")
        try:
            vacinas = []
            for x in range(len(dados_gato["vacinas"])):
                vacina = Vacinacao(dados_gato["datas_vacinas"][x], dados_gato["vacinas"][x], dados_gato["id"], tipo_animal="gato")
                vacinas.append(vacina)

            gato = Gato(dados_gato["id"], dados_gato["nome"], dados_gato["raca"], vacinas)
            conferir_gato = self.buscar_gato_por_id(gato.id)

            if conferir_gato is None:
                self.__gato_DAO.add(gato)
                if vacinas:
                    self.__vacinacao_DAO.add(vacinas)
                if modo == "doado":
                    return gato
            else:
                self.__tela_gato.erro("ID já cadastrado")
        except ValueError as ve:
            self.__tela_gato.erro(f"Erro nos dados fornecidos: {ve}")
        except Exception as e:
            self.__tela_gato.erro(f"Erro inesperado: {e}")


    def gerenciar_gatos(self):
        if not self.__gato_DAO.get_all():
            self.__tela_gato.erro("Nenhum gato cadastrado.")
            return

        gatos_formatados = []
        for gato in self.__gato_DAO.get_all():
            vacinas = ", ".join([f"{v.tipo_vacina.name} (Data: {v.dia_vacina.strftime('%d/%m/%Y')})" for v in gato.vacinas]) if gato.vacinas else "Nenhuma vacina"
            gatos_formatados.append({
                "id": gato.id, "nome": gato.nome, "raca": gato.raca, 
                "vacinas": vacinas
            })

        acao = self.__tela_gato.mostra_gato(gatos_formatados)
        if acao:
            tipo_acao, id_gato = acao
            if tipo_acao == "alterar":
                self.alterar_gato(id_gato)
            elif tipo_acao == "excluir":
                self.excluir_gato(id_gato)


    def alterar_gato(self, id): 
        gato = self.buscar_gato_por_id(id)
        if gato is None:
            self.__tela_gato.erro(idnotfound(gato.id))
            return 0

        # Abre a tela para editar os dados do gato
        gatoeditado = self.__tela_gato.pega_dados_gato(modo="alteracao",dados_existentes=gato.id)

        if not gatoeditado:  # Caso a edição seja cancelada
            return 0

        try:
            novas_vacinas = []
            for x in range(len(gatoeditado["vacinas"])):
                vacina_existente = next(
                    (v for v in gato.vacinas if v.tipo_vacina == gatoeditado["vacinas"][x]),
                    None
                )
                if vacina_existente:
                    vacina_existente.dia_vacina = gatoeditado["datas_vacinas"][x]
                else:
                    novas_vacinas.append(
                        Vacinacao(gatoeditado["datas_vacinas"][x],gatoeditado["vacinas"][x],gatoeditado["id"], tipo_animal="gato")
                    )

            gato.nome = gatoeditado["nome"]
            gato.raca = gatoeditado["raca"]
            gato.vacinas = novas_vacinas

            self.__gato_DAO.update(gato)
            # Registra no histórico as novas vacinações
            if novas_vacinas:
                self.__vacinacao_DAO.update(novas_vacinas)


            return 1
        except Exception as e:
            self.__tela_gato.erro(f"Erro ao alterar gato: {str(e)}")
            return 0


    def excluir_gato(self, id, modo = "excluir"):
        gato = self.buscar_gato_por_id(id)

        if(gato is not None):
            self.__gato_DAO.remove(gato.id)
            if modo == "excluir":
                self.__vacinacao_DAO.remove((gato.id,"gato"))
        else:
            self.__tela_gato.erro("ATENCAO: Gato não existente")


    def buscar_historico_vacinacao(self):
        if self.__vacinacao_DAO.get_all():  # Verifica se a lista não está vazia
            vacinas = []
            for i in self.__vacinacao_DAO.get_all():
                for j in i:
                    if j.tipo_animal == "gato":
                        adotado = self.buscar_gato_por_id(j.id_animal)
                        if adotado is None:
                            vacinas.append(f"Status: ADOTADO, Vacina: {j.tipo_vacina.name}, Data: {j.dia_vacina}, para o {j.tipo_animal} de ID: {j.id_animal}")
                        else:
                            vacinas.append(f"Vacina: {j.tipo_vacina.name}, Data: {j.dia_vacina}, para o {j.tipo_animal} de ID: {j.id_animal}")
            self.__tela_gato.exibir_vacinas("\n".join(vacinas))
        else:
            self.__tela_gato.exibir_vacinas("Histórico de vacinas vazio.")


    def buscar_gato_por_id(self, id):
        try:  
            gato = self.__gato_DAO.get(id)
            return gato
        except idnotfound:
            return None


    def retornar(self):
        self.__controlador_sistema.abre_tela()


    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_gato,
            2: self.gerenciar_gatos,
            3: self.buscar_historico_vacinacao,
            0: self.retornar
        }

        while True:
            opcao = self.__tela_gato.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)           
            funcao_escolhida()
