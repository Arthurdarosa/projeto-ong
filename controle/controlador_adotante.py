from limite.tela_adotante import TelaAdotante
from entidade.adotante import Adotante
from DAOs.adotante_dao import AdotanteDAO
from exceptions.CpfNotFound import cpfnotfound


class Controladoradotante():

    def __init__(self, controlador_sistema):
        self.__adotante_DAO = AdotanteDAO()
        self.__tela_adotante = TelaAdotante()
        self.__controlador_sistema = controlador_sistema

    def incluir_adotante(self):
        dados_adotante = self.__tela_adotante.pega_dados_adotante(modo="cadastro")
        adotante = Adotante(dados_adotante["nome"], dados_adotante["cpf"], dados_adotante["endereco"], dados_adotante["data_de_nascimento"], dados_adotante['tipo_moradia'], dados_adotante['outros_animais'])

        conferir_adotante = self.buscar_adotante_por_cpf(adotante.cpf)
        if conferir_adotante is None:
            self.__adotante_DAO.add(adotante)
            self.__tela_adotante.erro(f"Adotante {adotante.nome} cadastrado com sucesso!")

    def adotante_cadastrado(self):
        cpf_adotante = self.__tela_adotante.pega_cpf()
        adotante = self.buscar_adotante_por_cpf(cpf_adotante)
        if adotante == None:
            self.__tela_adotante.erro(cpfnotfound(adotante.cpf))
            return
        self.__controlador_sistema.dispatch_event("adotante_ja_cadastrado", adotante)


    def gerenciar_adotante(self):
        if not self.__adotante_DAO.get_all():
            self.__tela_adotante.erro("Nenhum adotante cadastrado.")
            return

        adotantes_formatados = []
        for adotante in self.__adotante_DAO.get_all():

            tipo_moradia = adotante.tipo_moradia
            if tipo_moradia:
                tipo_moradia_str = f"{tipo_moradia[0].name} - {tipo_moradia[1].name}"
            else:
                tipo_moradia_str = "Não informado"
            outros_animais = "Sim" if adotante.outros_animais else "Não"

            adotantes_formatados.append({
                "nome": adotante.nome, "cpf": adotante.cpf, 
                "endereco": adotante.endereco, "data_de_nascimento": adotante.data_de_nascimento,
                "tipo_moradia": tipo_moradia_str, "outros_animais": outros_animais
                })

        acao = self.__tela_adotante.mostra_adotante(adotantes_formatados)
        if acao:
            tipo_acao, cpf_adotante = acao
            if tipo_acao == "alterar":
                self.alterar_adotante(cpf_adotante)
            elif tipo_acao == "excluir":
                self.excluir_adotante(cpf_adotante)


    def alterar_adotante(self, cpf):
        adotante = self.buscar_adotante_por_cpf(cpf)
        if adotante is None:
            self.__tela_adotante.erro(cpfnotfound(adotante.cpf))
            return 0

        adotanteeditado = self.__tela_adotante.pega_dados_adotante(modo="alteracao",dados_existentes=adotante.cpf)

        if not adotanteeditado:
            return 0

        adotante.nome = adotanteeditado['nome']
        adotante.endereco = adotanteeditado['endereco']
        adotante.data_de_nascimento = adotanteeditado['data_de_nascimento']

        self.__adotante_DAO.update(adotante)

    def excluir_adotante(self, cpf):
        adotante = self.buscar_adotante_por_cpf(cpf)
        if(adotante is not None):
            self.__adotante_DAO.remove(adotante.cpf)
        else:
            self.__tela_adotante.erro(cpfnotfound(adotante.cpf))


    def buscar_adotante_por_cpf(self, cpf):
        adotante = self.__adotante_DAO.get(cpf)
        if isinstance(adotante, Adotante):
            return adotante
        return None

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_adotante,2: self.adotante_cadastrado,3: self.gerenciar_adotante, 0: self.retornar}

        while True:
            opcao = self.__tela_adotante.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_adotante.erro("Opção inválida. Tente novamente.")