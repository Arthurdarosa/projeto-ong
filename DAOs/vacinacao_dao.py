from DAOs.dao import DAO
from entidade.vacinacao import Vacinacao

class VacinacaoDAO(DAO):
    def __init__(self):
        super().__init__('vacinacao.pickle')

    def add(self, vacinas: list):
        if((vacinas is not None) and isinstance(vacinas, list) and isinstance (vacinas[0].id_animal, int) and isinstance(vacinas[0].tipo_animal, str)):
            super().add((vacinas[0].id_animal,vacinas[0].tipo_animal), vacinas)

    def update(self, vacinas: list):
        if((vacinas is not None) and isinstance(vacinas, list) and isinstance(vacinas[0].id_animal, int) and isinstance(vacinas[0].tipo_animal, str)):
            super().update((vacinas[0].id_animal,vacinas[0].tipo_animal), vacinas)

    def get(self, key: tuple):
        if isinstance(key, tuple):
            return super().get(key)

    def remove(self, key: tuple):
        if(isinstance(key, tuple)):
            return super().remove(key)