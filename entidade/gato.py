from .animal import *
from entidade.vacinacao import Vacinacao

class Gato(Animal):
    def __init__(self, id: int, nome: str, raca: str, vacinas: Vacinacao):
        super().__init__(id, nome, raca, vacinas)

        if all(isinstance(vacina, Vacinacao) for vacina in vacinas):
            self.__vacinas = vacinas
        else:
            raise ValueError("Vacinas deve ser uma lista de instâncias da classe Vacinacao.")

    @property
    def vacinas(self):
        return self.__vacinas

    @vacinas.setter
    def vacinas(self, value):
        if isinstance(value, list):
            self.__vacinas = value
        else:
            raise ValueError("Vacinas deve ser uma lista")
