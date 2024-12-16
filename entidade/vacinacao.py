from entidade.tipo_vacina import TipoVacina
from datetime import date

class Vacinacao:
    def __init__(self, dia_vacina: date, tipo_vacina: TipoVacina, id_animal: int, tipo_animal: str):
        
        self.__dia_vacina = None
        if isinstance(dia_vacina, date):
            self.__dia_vacina = dia_vacina
        else:
            raise ValueError("dia_vacina deve ser uma data")

        self.__tipo_vacina = None
        if isinstance(tipo_vacina, int):
            try:
                self.__tipo_vacina = TipoVacina(tipo_vacina)
            except ValueError:
                raise ValueError("tipo_vacina deve ser um dos valores do enum TipoVacina.")
        else:
            raise ValueError("tipo_vacina deve ser um número inteiro.")
        
        self.__id_animal = None
        if isinstance(id_animal, int):
            self.__id_animal = id_animal
        else:
            raise ValueError("id_animal deve ser um numero inteiro.")

        self.__tipo_animal = None
        if isinstance(tipo_animal, str):
            self.__tipo_animal = tipo_animal
        else:
            raise ValueError("tipo_animal deve ser uma string.")


    @property
    def dia_vacina(self):
        return self.__dia_vacina
    
    @dia_vacina.setter
    def dia_vacina(self, value):
        if isinstance(value, date):
            self.__dia_vacina = value
        else:
            raise ValueError("dia_vacina deve ser uma data")
    
    @property
    def tipo_vacina(self):
        return self.__tipo_vacina
    
    @tipo_vacina.setter
    def tipo_vacina(self, value):
        if isinstance(value, TipoVacina):
            self.__tipo_vacina = value
        else:
            raise ValueError("nome_vacina deve ser uma ")
    
    @property
    def id_animal(self):
        return self.__id_animal
    
    @id_animal.setter
    def id_animal(self, value):
        if isinstance(value, int):
            self.__id_animal = value
        else:
            raise ValueError("id_animal deve ser um numero inteiro")

    @property
    def tipo_animal(self):
        return self.__tipo_animal

    @tipo_animal.setter
    def tipo_animal(self, value):
        if isinstance(value, str):
            self.__tipo_animal = value
        else:
            raise ValueError("tipo_animal deve ser uma string")
