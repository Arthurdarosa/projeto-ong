from datetime import date
from .pessoa import Pessoa
from .tipo_moradia import *


class Adotante(Pessoa):
    def __init__(self, nome, cpf, endereco, data_de_nascimento, tipo_moradia, outros_animais):
        super().__init__(nome, cpf, endereco, data_de_nascimento)

        self.__tipo_moradia = None
        if isinstance(tipo_moradia, tuple) and len(tipo_moradia) == 2:
            tipo, tamanho = tipo_moradia
            if isinstance(tipo, int):
                try:
                    tipo = TipoMoradia(tipo)
                except ValueError:
                    raise ValueError("Tipo da moradia deve ser um dos valores do enum TipoMoradia.")
            else:
                raise ValueError("Tipo da moradia deve ser um número inteiro.")

            if isinstance(tamanho, int):
                try:
                    tamanho = TamanhoMoradia(tamanho)
                except ValueError:
                    raise ValueError("Tamanho da moradia deve ser um dos valores do enum TamanhoMoradia.")
            else:
                raise ValueError("Tamanho da moradia deve ser um número inteiro.")

            self.__tipo_moradia = (tipo, tamanho)
        else:
            raise ValueError("Tipo de moradia deve ser uma tupla com dois valores: TipoMoradia e TamanhoMoradia.")

        self.__outros_animais = None
        if isinstance(outros_animais, bool):
            self.__outros_animais = outros_animais
        else:
            raise ValueError("Outros animais deve ser um valor booleano")
        

    @property
    def tipo_moradia(self):
        return self.__tipo_moradia

    @tipo_moradia.setter
    def tipo_moradia(self, tipo_moradia):
        if isinstance(tipo_moradia, tuple) and len(tipo_moradia) == 2:
            tipo, tamanho = tipo_moradia
            if isinstance(tipo, TipoMoradia) and isinstance(tamanho, TamanhoMoradia):
                self.__tipo_moradia = (tipo, tamanho)
            else:
                raise ValueError("Tipo de moradia deve ser um enum TipoMoradia e TamanhoMoradia.")
        else:
            raise ValueError("Tipo de moradia deve ser uma tupla com dois valores: TipoMoradia e TamanhoMoradia.")

    @property
    def outros_animais(self):
        return self.__outros_animais

    @outros_animais.setter
    def outros_animais(self, outros_animais: bool):
        if isinstance(outros_animais, bool):
            self.__outros_animais = outros_animais
        else:
            raise ValueError("Outros animais deve ser um valor booleano")