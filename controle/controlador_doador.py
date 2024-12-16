from limite.tela_doador import TelaDoador
from entidade.doador import Doador
from DAOs.doador_dao import DoadorDAO
from exceptions.CpfNotFound import *


class Controladordoador():

    def __init__(self, controlador_sistema):
        self.__doador_DAO = DoadorDAO()
        self.__tela_doador = TelaDoador()
        self.__controlador_sistema = controlador_sistema


    def incluir_doador(self):
        dados_doador = self.__tela_doador.pega_dados_doador(modo="cadastro")
        doador = Doador(dados_doador["nome"], dados_doador["cpf"], dados_doador["endereco"], dados_doador["data_de_nascimento"])

        conferir_doador = self.buscar_doador_por_cpf(doador.cpf)
        if conferir_doador is None:
            self.__doador_DAO.add(doador)
            self.__tela_doador.erro(f"Doador {doador.nome} cadastrado com sucesso!")

    def doador_cadastrado(self):
        cpf_doador = self.__tela_doador.pega_cpf()
        doador = self.buscar_doador_por_cpf(cpf_doador)
        if doador == None:
            self.__tela_doador.erro(cpfnotfound(cpf_doador))
            return
        gato_ou_cachorro = self.__tela_doador.gato_ou_cachorro()
        if gato_ou_cachorro == 0:
            self.__controlador_sistema.dispatch_event("doador_cadastrado_cachorro", doador)
        elif gato_ou_cachorro == 1:
            self.__controlador_sistema.dispatch_event("doador_cadastrado_gato", doador)


    def gerenciar_doador(self):
        if not self.__doador_DAO.get_all():
            self.__tela_doador.erro("Nenhum doador cadastrado.")
            return

        doadores_formatados = []
        for doador in self.__doador_DAO.get_all():
            doadores_formatados.append({
                "nome": doador.nome, "cpf": doador.cpf, 
                "endereco": doador.endereco, "data_de_nascimento": doador.data_de_nascimento
                })

        acao = self.__tela_doador.mostra_doador(doadores_formatados)
        if acao:
            tipo_acao, cpf_doador = acao
            if tipo_acao == "alterar":
                self.alterar_doador(cpf_doador)
            elif tipo_acao == "excluir":
                self.excluir_doador(cpf_doador)


    def alterar_doador(self, cpf):
        doador = self.buscar_doador_por_cpf(cpf)
        if doador is None:
            self.__tela_doador.erro(cpfnotfound(cpf))
            return 0

        doadoreditado = self.__tela_doador.pega_dados_doador(modo="alteracao",dados_existentes=doador.cpf)

        if not doadoreditado:
            return 0

        doador.nome = doadoreditado['nome']
        doador.endereco = doadoreditado['endereco']
        doador.data_de_nascimento = doadoreditado['data_de_nascimento']

        self.__doador_DAO.update(doador)

    def excluir_doador(self, cpf):
        doador = self.buscar_doador_por_cpf(cpf)
        if(doador is not None):
            self.__doador_DAO.remove(doador.cpf)
        else:
            self.__tela_doador.erro(cpfnotfound(cpf))


    def buscar_doador_por_cpf(self, cpf):
        doador = self.__doador_DAO.get(cpf)
        if isinstance(doador, Doador):
            return doador
        return None


    def retornar(self):
        self.__controlador_sistema.abre_tela()


    def abre_tela(self):
        lista_opcoes = {1: self.incluir_doador,2: self.doador_cadastrado,3: self.gerenciar_doador, 0: self.retornar}

        while True:
            opcao = self.__tela_doador.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_doador.erro("Opção inválida. Tente novamente.")