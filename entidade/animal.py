from abc import ABC, abstractmethod



class Animal(ABC):
    def __init__(self, id: int, nome: str, raca: str, vacinas=None):
        self.__id = None
        if isinstance(id, int):
            self.__id = id
        else:
            raise ValueError("ID não é válido")

        self.__nome = None
        if isinstance(nome, str):
            self.__nome = nome
        else:
            raise ValueError("Nome não é válido")

        self.__raca = None
        if isinstance(raca, str):
            self.__raca = raca
        else:
            raise ValueError("Raça não é válida")

        self.__vacinas = vacinas if vacinas is not None else []
        self.historico_vacinacao = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self.__id = value
        else:
            raise ValueError("ID não é válido")

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        if isinstance(value, str):
            self.__nome = value
        else:
            raise ValueError("Nome não é válido")

    @property
    def raca(self):
        return self.__raca

    @raca.setter
    def raca(self, value):
        if isinstance(value, str):
            self.__raca = value
        else:
            raise ValueError("Raça não é válida")

    @property
    def vacinas(self):
        return self.__vacinas

    @vacinas.setter
    def vacinas(self, value):
        if isinstance(value, list):
            self.__vacinas = value
        else:
            raise ValueError("Vacinas devem ser uma lista.")


