import PySimpleGUI as sg
from datetime import date
from exceptions.CpfNotFound import *


class TelaDoador:

    def tela_opcoes(self):
        layout = [
            [sg.Text("----Doar Animal----")],
            [sg.Text("Faça o Login para continuar para Doação.")],
            [sg.Button("Cadastrar Doador"), sg.Button("Fazer Login"),sg.Button("Gerenciar doadores cadastrados"), sg.Button("Retornar")]
        ]

        window = sg.Window("Opções de Doador", layout)

        while True:
            event, _ = window.read()

            if event == sg.WINDOW_CLOSED or event == "Retornar":
                window.close()
                return 0
            elif event == "Cadastrar Doador":
                window.close()
                return 1
            elif event == "Fazer Login":
                window.close()
                return 2
            elif event == "Gerenciar doadores cadastrados":
                window.close()
                return 3

    def pega_dados_doador(self, modo = "cadastro", dados_existentes = None):
        cpf_disabled = (modo == "alteracao")
        layout = [
            [sg.Text("---------- DADOS DOADOR ----------")],
            [sg.Text("Nome:"), sg.InputText("", key="nome")],
            [sg.Text("CPF (número inteiro):"), sg.InputText(
            dados_existentes if dados_existentes else "",
            key="cpf", disabled=cpf_disabled)],
            [sg.Text("Endereço:"), sg.InputText("", key="endereco")],
            [sg.Text("Data de Nascimento (dd/mm/aaaa):"), sg.InputText("", key="data_de_nascimento")],
            [sg.Button("Cadastrar")]
        ]

        window = sg.Window("Cadastro de Doador", layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                window.close()
                break

            if event == "Cadastrar":
                try:
                    try:
                        cpf = int(values["cpf"])  # Tenta converter o valor para inteiro
                    except ValueError:
                        raise ValueError("cpf são numeros amigão! ")
                    # Validar Data de Nascimento
                    partes_data = values["data_de_nascimento"].split('/')
                    if len(partes_data) == 3:
                        dia, mes, ano = map(int, partes_data)
                        data_de_nascimento = date(ano, mes, dia)
                    else:
                        raise ValueError("Formato de data inválido. Por favor, insira no formato dd/mm/aaaa.")

                    window.close()

                    return {
                        "nome": values["nome"],
                        "cpf": cpf,
                        "endereco": values["endereco"],
                        "data_de_nascimento": data_de_nascimento
                    }

                    
                except ValueError as e:
                    sg.popup(f"Erro: {e}. Tente novamente.")

        window.close()


    def janela_opcoes(self, doador):
        layout = [
            [sg.Text(f"Você escolheu {doador['nome']}.")],
            [sg.Text(f"CPF: {doador['cpf']}")],
            [sg.Text(f"Endereço: {doador['endereco']}")],
            [sg.Text(f"Data de Nascimento: {doador['data_de_nascimento']}")],
            [sg.Button("Alterar"), sg.Button("Excluir"),sg.Button("Cancelar")],
        ]
        window = sg.Window(f"Doador selecionado: {doador['nome']}", layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None  # Nenhuma ação
            elif event == "Alterar":
                window.close()
                return ("alterar", doador["cpf"])
            elif event == "Excluir":
                window.close()
                return ("excluir", doador["cpf"])


    def mostra_doador(self, doadores):
        layout = [
            [sg.Text("Lista de Doadores Cadastrados:")],
            [
                sg.Listbox(
                        values=[f"{doador['cpf']} - {doador['nome']} - {doador['endereco']} - {doador['data_de_nascimento']}" for doador in doadores],
                        size=(50, len(doadores)),
                        key="doador_selecionado",
                        enable_events=True,
                )
            ],
            [sg.Button("Fechar"),sg.Button("Buscar por CPF")]
        ]

        window = sg.Window("Listagem de Doadores", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Fechar"):
                break
            elif event == "doador_selecionado":
                selecao = values["doador_selecionado"]
                if selecao:
                    cpf_doador = int(selecao[0].split(" - ")[0])
                    doador = next(d for d in doadores if d["cpf"] == cpf_doador)
                    acao = self.janela_opcoes(doador)
                    if acao:
                        window.close()
                        return acao
            elif event == "Buscar por CPF":
                try:
                    cpf_doador = self.pega_cpf()
                    doador = next(d for d in doadores if d["cpf"] == cpf_doador)
                    acao = self.janela_opcoes(doador)
                    if acao:
                        window.close()
                        return acao
                except ValueError:
                    self.erro("CPF inválido! Por favor, insira um número válido.")
                except StopIteration:
                    self.erro(cpfnotfound(cpf_doador))

        window.close()

    def pega_cpf(self):
        layout = [
            [sg.Text("Digite o CPF do doador cadastrado:")],
            [sg.InputText("", key="cpf")],
            [sg.Button("Buscar"), sg.Button("Cancelar")]
        ]

        self.window = sg.Window("Buscar doador", layout)

        while True:
            event, values = self.window.read()

            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                self.window.close()
                return None  # Se o usuário cancelar ou fechar a janela

            if event == "Buscar":
                try:
                    cpf_doador = int(values["cpf"])
                    self.window.close()
                    return cpf_doador
                except ValueError:
                    sg.popup("Por favor, insira um CPF válido.")

    def gato_ou_cachorro(self):
        layout = [
            [sg.Button("Doar Gato", key="Doar_Gato",  size=(20, 1))],
            [sg.Button("Doar Cachorro", key="Doar_Cachorro",  size=(20, 1))]
        ]

        window = sg.Window("Escolha entre Doar Gato ou Cachorro", layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                window.close()
                break

            if event == "Doar_Gato":
                window.close()
                return 1
            else:
                window.close()
                return 0

        window.close()


    def erro(self, valor):
        sg.popup(valor)