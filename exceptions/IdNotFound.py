class idnotfound(Exception):
    def __init__(self, mensagem):
        self.mensagem = f"o id {mensagem} nao foi encontrado"
        super().__init__(self.mensagem)