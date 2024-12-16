import PySimpleGUI as sg
from datetime import date
from exceptions.CpfNotFound import *


class TelaAdotante:

    def tela_opcoes(self):
        layout = [
            [sg.Text("Cadastrar adotante")],
            [sg.Text("Fazer Login Adotante")],
            [sg.Button("Cadastrar Adotante"), sg.Button("Fazer Login"), sg.Button("Gerenciar Adotantes"), sg.Button("Retornar")]
        ]

        window = sg.Window("Opções de Adotante", layout)

        while True:
            event, _ = window.read()

            if event == sg.WINDOW_CLOSED or event == "Retornar":
                window.close()
                return 0
            elif event == "Cadastrar Adotante":
                window.close()
                return 1
            elif event == "Fazer Login":
                window.close()
                return 2
            elif event == "Gerenciar Adotantes":
                window.close()
                return 3


        window.close()


    def pega_dados_adotante(self, modo = "cadastro", dados_existentes = None):
        cpf_disabled = (modo == "alteracao")
        layout = [
            [sg.Text("---------- DADOS ADOTANTE ----------")],
            [sg.Text("Nome:"), sg.InputText("", key="nome")],
            [sg.Text("CPF (número inteiro):"), sg.InputText(
            dados_existentes if dados_existentes else "",
            key="cpf", disabled=cpf_disabled)],
            [sg.Text("Endereço:"), sg.InputText("", key="endereco")],
            [sg.Text("Data de Nascimento (dd/mm/aaaa):"), sg.InputText("", key="data_de_nascimento")],
            [
                sg.Text("Tipo de Moradia:"),
                sg.Combo(["1 - Casa", "2 - Apartamento"], key="tipo", readonly=True),
            ],
            [
                sg.Text("Tamanho de Moradia:"),
                sg.Combo(["1 - Pequeno", "2 - Médio","3 - Grande"], key="tamanho", readonly=True),
            ],
            [
                sg.Text("Possui outros animais:"),
                sg.Combo(["1 - Sim","2 - Não"], key="outros_animais", readonly=True),
            ],
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
                        idade = self.calcula_idade(data_de_nascimento)

                        if idade < 18:
                            window.close()
                            sg.popup("O adotante precisa ter pelo menos 18 anos.")
                            return
                    else:
                        raise ValueError("Formato de data inválido. Por favor, insira no formato dd/mm/aaaa.")

                    tipo_selecionado = values["tipo"]
                    if tipo_selecionado:
                        tipo_inteiro = int(tipo_selecionado.split(" - ")[0])
                    else:
                        raise ValueError("Por favor, selecione um tipo válido.")

                    tamanho_selecionado = values["tamanho"]
                    if tamanho_selecionado:
                        tamanho_inteiro = int(tamanho_selecionado.split(" - ")[0])
                    else:
                        raise ValueError("Por favor, selecione um tamanho válido.")

                    tipo_moradia = (tipo_inteiro,tamanho_inteiro)

                    outros_selecionado = values["outros_animais"]
                    if outros_selecionado:
                        outros_inteiro = int(outros_selecionado.split(" - ")[0])
                    else:
                        raise ValueError("Por favor, selecione 'Sim' ou 'Não' válido.")
                    
                    outros_animais = True if outros_inteiro == 1 else False

                    window.close()

                    return {
                        "nome": values["nome"],
                        "cpf": cpf,
                        "endereco": values["endereco"],
                        "data_de_nascimento": data_de_nascimento,
                        "tipo_moradia": tipo_moradia,
                        "outros_animais": outros_animais
                    }

                    
                except ValueError as e:
                    sg.popup(f"Erro: {e}. Tente novamente.")

        window.close()


    def janela_opcoes(self, adotante):
        layout = [
            [sg.Text(f"Você escolheu {adotante['nome']}.")],
            [sg.Text(f"CPF: {adotante['cpf']}")],
            [sg.Text(f"Endereço: {adotante['endereco']}")],
            [sg.Text(f"Data de Nascimento: {adotante['data_de_nascimento']}")],
            [sg.Text(f"Moradia: {adotante['tipo_moradia']}")],
            [sg.Text(f"Outros Animais: {adotante['outros_animais']}")],
            [sg.Button("Alterar"), sg.Button("Excluir"),sg.Button("Cancelar")],
        ]
        window = sg.Window(f"Adotante selecionado: {adotante['nome']}", layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None  # Nenhuma ação
            elif event == "Alterar":
                window.close()
                return ("alterar", adotante["cpf"])
            elif event == "Excluir":
                window.close()
                return ("excluir", adotante["cpf"])


    def mostra_adotante(self, adotantes):
        layout = [
            [sg.Text("Lista de Adotantes Cadastrados:")],
            [
                sg.Listbox(
                        values=[f"{adotante['cpf']} - {adotante['nome']} - {adotante['endereco']} - {adotante['data_de_nascimento']} - {adotante['tipo_moradia']} - Outros Animais: {adotante['outros_animais']}" for adotante in adotantes],
                        size=(50, len(adotantes)),
                        key="adotante_selecionado",
                        enable_events=True,
                )
            ],
            [sg.Button("Fechar"),sg.Button("Buscar por CPF")]
        ]

        window = sg.Window("Listagem de Adotantes", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Fechar"):
                break
            elif event == "adotante_selecionado":
                selecao = values["adotante_selecionado"]
                if selecao:
                    cpf_adotante = int(selecao[0].split(" - ")[0])
                    adotante = next(a for a in adotantes if a["cpf"] == cpf_adotante)
                    acao = self.janela_opcoes(adotante)
                    if acao:
                        window.close()
                        return acao
            elif event == "Buscar por CPF":
                try:
                    cpf_adotante = self.pega_cpf()
                    adotante = next(a for a in adotantes if a["cpf"] == cpf_adotante)
                    acao = self.janela_opcoes(adotante)
                    if acao:
                        window.close()
                        return acao
                except ValueError:
                    self.erro("CPF inválido! Por favor, insira um número válido.")
                except StopIteration:
                    self.erro(cpfnotfound(cpf_adotante))

        window.close()


    def pega_cpf(self):
        layout = [
            [sg.Text("Digite o CPF do adotante cadastrado:")],
            [sg.InputText("", key="cpf")],
            [sg.Button("Buscar"), sg.Button("Cancelar")]
        ]

        self.window = sg.Window("Buscar adotante", layout)

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


    def calcula_idade(self, data_de_nascimento):
        today = date.today()
        idade = today.year - data_de_nascimento.year
        if today.month < data_de_nascimento.month or (today.month == data_de_nascimento.month and today.day < data_de_nascimento.day):
            idade -= 1
        return idade


    def erro(self, valor):
        sg.popup(valor)
