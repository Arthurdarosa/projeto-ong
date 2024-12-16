from entidade.animal import *
from entidade.porte import Porte
from entidade.vacinacao import Vacinacao

class Cachorro(Animal):
    def __init__(self, id, nome, raca, porte, vacinas):
        super().__init__(id, nome, raca, vacinas)

        self.__porte = None
        if isinstance(porte, int):
            try:
                self.__porte = Porte(porte)
            except ValueError:
                raise ValueError("Porte deve ser um dos valores do enum Porte.")
        else:
            raise ValueError("Porte deve ser um número inteiro.")

        if all(isinstance(vacina, Vacinacao) for vacina in vacinas):
            self.__vacinas = vacinas
        else:
            raise ValueError("Vacinas deve ser uma lista de instâncias da classe Vacinacao.")

    @property
    def porte(self):
        return self.__porte

    @porte.setter
    def porte(self, value):
        if isinstance(value, Porte):
            self.__porte = value
        else:
            raise ValueError("Porte deve ser um dos valores do enum Porte.")
    
    @property
    def vacinas(self):
        return self.__vacinas
    
    @vacinas.setter
    def vacinas(self, value):
        if isinstance(value, list):
            self.__vacinas = value
        else:
            raise ValueError("Vacinas deve ser uma lista")

