from datetime import date
from .pessoa import Pessoa

class Doador(Pessoa):
    def __init__(self, nome: str, cpf: int, endereco: str, data_de_nascimento: date):
        super().__init__(nome, cpf, endereco, data_de_nascimento)