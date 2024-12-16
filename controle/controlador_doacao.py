from entidade.doacao import Doacao
from entidade.cachorro import Cachorro
from entidade.gato import Gato
from DAOs.doacao_dao import DoacaoDAO
from limite.tela_doacao import TelaDoacao

class ControladorDoacao:

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__doacao_DAO = DoacaoDAO()
        self.__tela_doacao = TelaDoacao()

    def cadastrar_doacao_com_cachorro(self, doador):
        controlador_cachorro = self.__controlador_sistema.controlador_cachorro
        cachorro = controlador_cachorro.incluir_cachorro(modo="doado")
        
        if isinstance(cachorro, Cachorro):
            dados_doacao = self.__tela_doacao.pega_dados_doacao()
            doacao = Doacao(dados_doacao["data"], dados_doacao["motivo"], doador, cachorro)  # Cria a doação
            self.__doacao_DAO.add(doacao)
            
            return cachorro
        else:
            return None

    def cadastrar_doacao_com_gato(self, doador):
        controlador_gato = self.__controlador_sistema.controlador_gato
        gato = controlador_gato.incluir_gato(modo="doado")

        if isinstance(gato, Gato):
            dados_doacao = self.__tela_doacao.pega_dados_doacao()
            doacao = Doacao(dados_doacao["data"], dados_doacao["motivo"], doador, gato)
            self.__doacao_DAO.add(doacao)

            return gato
        else:
            return None


    