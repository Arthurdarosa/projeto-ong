class cpfnotfound(Exception):
    def __init__(self, cpf):
        self.mensagem = f"o cpf {cpf} nao foi encontrado"
        super().__init__(self.mensagem)