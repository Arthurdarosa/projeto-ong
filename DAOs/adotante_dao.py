from DAOs.dao import DAO
from entidade.adotante import Adotante

class AdotanteDAO(DAO):
    def __init__(self):
        super().__init__('adotante.pickle')


    def add(self, adotante: Adotante):
        if((adotante is not None) and isinstance(adotante, Adotante) and isinstance (adotante.cpf, int)):
            super().add(adotante.cpf, adotante)

    def update(self, adotante: Adotante):
        if((adotante is not None) and isinstance(adotante, Adotante) and isinstance(adotante.cpf, int)):
            super().update(adotante.cpf, adotante)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)