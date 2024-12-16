from DAOs.dao import DAO
from entidade.doacao import Doacao

class DoacaoDAO(DAO):
    def __init__(self):
        super().__init__('doacao.pickle')

    def add(self, doacao: Doacao):
        chave = doacao.gerar_chave_unica()
        if((doacao is not None) and isinstance(doacao, Doacao)):
            super().add(chave, doacao)

    def update(self, doacao: Doacao):
        chave = doacao.gerar_chave_unica()
        if((doacao is not None) and isinstance(doacao, Doacao)):
            super().update(chave, doacao)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)