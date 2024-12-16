from entidade.vacinacao import *
from animal import *
from doacao import *
from adocao import *
from doador import *
from adotante import *


adotante = Adotante("João Silva", 12345678901, "Rua A, 123", date(1990, 1, 1), "Casa", True)
doador = Doador("Maria Oliveira", 10987654321, "Rua B, 456", date(1985, 5, 15))

print(adotante.endereco)
print(doador.cpf)