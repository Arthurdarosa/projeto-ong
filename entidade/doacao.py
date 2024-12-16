from datetime import date
from entidade.gato import *
from entidade.cachorro import *
from entidade.doador import *


class Doacao:
    def __init__(self, data_de_doacao: date, motivo: str, doador, animal):
        # Validações
        if not isinstance(data_de_doacao, date):
            raise ValueError("data_de_doacao deve ser uma instância de date")
        self.__data_de_doacao = data_de_doacao

        if not isinstance(motivo, str):
            raise ValueError("motivo deve ser uma string")
        self.__motivo = motivo

        if not isinstance(doador, Doador):
            raise ValueError("doador deve ser uma instância de Doador")
        self.__doador = doador

        if not isinstance(animal, (Gato, Cachorro)):
            raise ValueError("animal deve ser uma instância de Gato ou Cachorro")
        self.__animal = animal

    # Getters
    @property
    def data_de_doacao(self) -> date:
        return self.__data_de_doacao

    @property
    def motivo(self) -> str:
        return self.__motivo

    @property
    def doador(self):
        return self.__doador

    @property
    def animal(self):
        return self.__animal

    # Setters
    @data_de_doacao.setter
    def data_de_doacao(self, data_de_doacao: date):
        if isinstance(data_de_doacao, date):
            self.__data_de_doacao = data_de_doacao
        else:
            raise ValueError("data_de_doacao deve ser uma instância de date")

    @motivo.setter
    def motivo(self, motivo: str):
        if isinstance(motivo, str):
            self.__motivo = motivo
        else:
            raise ValueError("motivo deve ser uma string")

    @doador.setter
    def doador(self, doador):
        if isinstance(doador, Doador):
            self.__doador = doador
        else:
            raise ValueError("doador deve ser uma instância de Doador")
        
    def gerar_chave_unica(self):
        prefixo = "G-" if isinstance(self.animal, Gato) else "C-"
        return f"{prefixo}{self.animal.id}"