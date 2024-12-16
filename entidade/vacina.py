class Vacina:
    def __init__(self, dia_vacina, nome_vacina, id_animal):
        self.__dia_vacina = None
        if isinstance(dia_vacina, str):
            self.__dia_vacina = dia_vacina
        else:
            raise ValueError("dia_vacina deve ser uma string representando a data")

        self.__nome_vacina = None
        if isinstance(nome_vacina, str):
            self.__nome_vacina = nome_vacina
        else:
            raise ValueError("nome_vacina deve ser uma string")

        self.__id_animal = None
        if isinstance(id_animal, int):
            self.__id_animal = id_animal
        else:
            raise ValueError("id_animal deve ser um número inteiro")
    
    @property
    def dia_vacina(self):
        return self.__dia_vacina
    
    @dia_vacina.setter
    def dia_vacina(self, value):
        if isinstance(value, str):
            self.__dia_vacina = value
        else:
            raise ValueError("dia_vacina deve ser uma string representando a data")
    
    @property
    def nome_vacina(self):
        return self.__nome_vacina
    
    @nome_vacina.setter
    def nome_vacina(self, value):
        if isinstance(value, str):
            self.__nome_vacina = value
        else:
            raise ValueError("nome_vacina deve ser uma string")
    
    @property
    def id_animal(self):
        return self.__id_animal
    
    @id_animal.setter
    def id_animal(self, value):
        if isinstance(value, int):
            self.__id_animal = value
        else:
            raise ValueError("id_animal deve ser um número inteiro")
