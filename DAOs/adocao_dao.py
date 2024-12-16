from DAOs.dao import DAO
from entidade.adocao import Adocao

class AdocaoDAO(DAO):
    def __init__(self):
        super().__init__('adocao.pickle')

    def add(self, adocao: Adocao):
        chave = adocao.gerar_chave_unica()
        if((adocao is not None) and isinstance(adocao, Adocao)):
            super().add(chave, adocao)

    def update(self, adocao: Adocao):
        chave = adocao.gerar_chave_unica()
        if((adocao is not None) and isinstance(adocao, Adocao)):
            super().update(chave, adocao)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)