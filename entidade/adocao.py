from datetime import date
from entidade.adotante import *
from entidade.gato import *
from entidade.cachorro import *

class Adocao:
    def __init__(self, data_de_adocao, animal, adotante, termo_responsabilidade):
        self.__data_de_adocao = None
        if isinstance(data_de_adocao, date):
            self.__data_de_adocao = data_de_adocao
        else:
            raise ValueError("data_de_adocao deve ser uma instância de date")

        self.__animal = None
        if isinstance(animal, (Gato, Cachorro)):
            self.__animal = animal
        else:
            raise ValueError("animal deve ser uma instância de Gato ou Cachorro")

        self.__adotante = None
        if isinstance(adotante, Adotante):
            self.__adotante = adotante
        else:
            raise ValueError("adotante deve ser uma instância de Adotante")

        self.__termo_responsabilidade = None
        if isinstance(termo_responsabilidade, bool):
            self.__termo_responsabilidade = termo_responsabilidade
        else:
            raise ValueError("termo_responsabilidade deve ser um booleano")

    @property
    def data_de_adocao(self):
        return self.__data_de_adocao

    @property
    def animal(self):
        return self.__animal

    @property
    def adotante(self):
        return self.__adotante

    @property
    def termo_responsabilidade(self):
        return self.__termo_responsabilidade

    # Setters
    @data_de_adocao.setter
    def data_de_adocao(self, data_de_adocao):
        if isinstance(data_de_adocao, date):
            self.__data_de_adocao = data_de_adocao
        else:
            raise ValueError("data_de_adocao deve ser uma instância de date")

    @animal.setter
    def animal(self, animal):
        if isinstance(animal, (Gato, Cachorro)):
            self.__animal = animal
            self.validar_adocao()
        else:
            raise ValueError("animal deve ser uma instância de Gato ou Cachorro")

    @adotante.setter
    def adotante(self, adotante):
        if isinstance(adotante, Adotante):
            self.__adotante = adotante
        else:
            raise ValueError("adotante deve ser uma instância de Adotante")

    @termo_responsabilidade.setter
    def termo_responsabilidade(self, termo_responsabilidade):
        if isinstance(termo_responsabilidade, bool):
            self.__termo_responsabilidade = termo_responsabilidade
        else:
            raise ValueError("termo_responsabilidade deve ser um booleano")
    
    def gerar_chave_unica(self):
        prefixo = "G-" if isinstance(self.animal, Gato) else "C-"
        return f"{prefixo}{self.animal.id}"

    