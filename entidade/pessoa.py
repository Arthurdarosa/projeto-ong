from abc import ABC, abstractmethod
from datetime import date

class Pessoa(ABC):
    def __init__(self, nome, cpf, endereco, data_de_nascimento):
        self.__nome = None
        if isinstance(nome, str):
            self.__nome = nome
        else:
            raise ValueError("Nome deve ser uma string")

        self.__cpf = None
        if isinstance(cpf, int):
            self.__cpf = cpf
        else:
            raise ValueError("CPF deve ser um número inteiro")

        self.__endereco = None
        if isinstance(endereco, str):
            self.__endereco = endereco
        else:
            raise ValueError("Endereço deve ser uma string")

        self.__data_de_nascimento = None
        if isinstance(data_de_nascimento, date):
            self.__data_de_nascimento = data_de_nascimento
        else:
            raise ValueError("Data de nascimento deve ser uma data")

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if isinstance(nome, str):
            self.__nome = nome
        else:
            raise ValueError("Nome deve ser uma string")

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if isinstance(cpf, int):
            self.__cpf = cpf
        else:
            raise ValueError("CPF deve ser um número inteiro")

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        if isinstance(endereco, str):
            self.__endereco = endereco
        else:
            raise ValueError("Endereço deve ser uma string")

    @property
    def data_de_nascimento(self):
        return self.__data_de_nascimento

    @data_de_nascimento.setter
    def data_de_nascimento(self, data: date):
        if isinstance(data, date):
            self.__data_de_nascimento = data
        else:
            raise ValueError("Data de nascimento deve ser uma data")