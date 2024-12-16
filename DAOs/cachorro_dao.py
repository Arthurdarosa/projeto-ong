from DAOs.dao import DAO
from entidade.cachorro import Cachorro

class CachorroDAO(DAO):
    def __init__(self):
        super().__init__('cachorro.pickle')

    def add(self, cachorro: Cachorro):
        if((cachorro is not None) and isinstance(cachorro, Cachorro) and isinstance (cachorro.id, int)):
            super().add(cachorro.id, cachorro)

    def update(self, cachorro: Cachorro):
        if((cachorro is not None) and isinstance(cachorro, Cachorro) and isinstance(cachorro.id, int)):
            super().update(cachorro.id, cachorro)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)