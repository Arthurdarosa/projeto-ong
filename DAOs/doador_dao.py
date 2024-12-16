from DAOs.dao import DAO
from entidade.doador import Doador

class DoadorDAO(DAO):
    def __init__(self):
        super().__init__('doador.pickle')


    def add(self, doador: Doador):
        if((doador is not None) and isinstance(doador, Doador) and isinstance (doador.cpf, int)):
            super().add(doador.cpf, doador)

    def update(self, doador: Doador):
        if((doador is not None) and isinstance(doador, Doador) and isinstance(doador.cpf, int)):
            super().update(doador.cpf, doador)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)