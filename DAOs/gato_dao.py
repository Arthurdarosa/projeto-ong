from DAOs.dao import DAO
from entidade.gato import Gato

class GatoDAO(DAO):
    def __init__(self):
        super().__init__('gato.pickle')


    def add(self, gato: Gato):
        if((gato is not None) and isinstance(gato, Gato) and isinstance (gato.id, int)):
            super().add(gato.id, gato)

    def update(self, gato: Gato):
        if((gato is not None) and isinstance(gato, Gato) and isinstance(gato.id, int)):
            super().update(gato.id, gato)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)