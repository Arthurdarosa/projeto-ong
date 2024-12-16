import PySimpleGUI as sg
from datetime import date
from exceptions.IdNotFound import *


class TelaAdocao:

    def janela_opcoes_gato(self, gato):
        layout = [
            [sg.Text(f"Você escolheu {gato['nome']}.")],
            [sg.Text(f"ID: {gato['id']}")],
            [sg.Text(f"Raça: {gato['raca']}")],
            [sg.Text(f"Vacinas: {gato['vacinas']}")],
            [sg.Button("Adotar"), sg.Button("Cancelar")],
        ]
        window = sg.Window(f"Gato selecionado: {gato['nome']}", layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None  # Nenhuma ação
            elif event == "Adotar":
                window.close()
                return (gato["id"])


    def mostra_gato(self, gatos):
        layout = [
            [sg.Text("Lista de Gatos Disponíveis:")],
            [
                sg.Listbox(
                        values=[f"{gato['id']} - Nome: {gato['nome']}, Raça: {gato['raca']}, Vacinas: {gato['vacinas']}" for gato in gatos],
                        size=(50, len(gatos)),
                        key="gato_selecionado",
                        enable_events=True,
                )
            ],
            [sg.Button("Fechar"),sg.Button("Buscar por ID")]
        ]

        window = sg.Window("Listagem de Gatos", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Fechar"):
                break
            elif event == "gato_selecionado":
                selecao = values["gato_selecionado"]
                if selecao:
                    id_gato = int(selecao[0].split(" - ")[0])
                    gato = next(g for g in gatos if g["id"] == id_gato)
                    acao = self.janela_opcoes_gato(gato)
                    if acao:
                        window.close()
                        return acao
            elif event == "Buscar por ID":
                try:
                    id_gato = self.pega_id_gato()
                    gato = next(g for g in gatos if g["id"] == id_gato)
                    acao = self.janela_opcoes_gato(gato)
                    if acao:
                        window.close()
                        return acao
                except ValueError:
                    self.erro("ID inválido! Por favor, insira um número válido.")
                except StopIteration:
                    self.erro(idnotfound(id_gato))

        window.close()

    
    def janela_opcoes_cachorro(self, cachorro):
        layout = [
            [sg.Text(f"Você escolheu {cachorro['nome']}.")],
            [sg.Text(f"ID: {cachorro['id']}")],
            [sg.Text(f"Raça: {cachorro['raca']}")],
            [sg.Text(f"Porte: {cachorro['porte']}")],
            [sg.Text(f"Vacinas: {cachorro['vacinas']}")],
            [sg.Button("Adotar"),sg.Button("Cancelar")],
        ]
        window = sg.Window(f"Cachorro selecionado: {cachorro['nome']}", layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None 
            elif event == "Adotar":
                window.close()
                return (cachorro["id"])


    def mostra_cachorro(self, cachorros):
        layout = [
            [sg.Text("Lista de Cachorros Disponíveis:")],
            [
                sg.Listbox(
                        values=[f"{cachorro['id']} - Nome: {cachorro['nome']}, Raça: {cachorro['raca']}, Porte: {cachorro['porte']}, Vacinas: {cachorro['vacinas']}" for cachorro in cachorros],
                        size=(50, len(cachorros)),
                        key="cachorro_selecionado",
                        enable_events=True,
                )
            ],
            [sg.Button("Fechar"),sg.Button("Buscar por ID")]
        ]

        window = sg.Window("Listagem de Cachorros", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Fechar"):
                break
            elif event == "cachorro_selecionado":
                # Obtém o animal selecionado
                selecao = values["cachorro_selecionado"]
                if selecao:
                    id_cachorro = int(selecao[0].split(" - ")[0])
                    cachorro = next(c for c in cachorros if c["id"] == id_cachorro)
                    acao = self.janela_opcoes_cachorro(cachorro)
                    if acao:
                        window.close()
                        return acao
            elif event == "Buscar por ID":
                try:
                    id_cachorro = self.pega_id_cachorro()
                    cachorro = next(c for c in cachorros if c["id"] == id_cachorro)
                    acao = self.janela_opcoes_cachorro(cachorro)
                    if acao:
                        window.close()
                        return acao
                except ValueError:
                    self.erro("ID inválido! Por favor, insira um número válido.")
                except StopIteration:
                    self.erro(idnotfound(id_cachorro))

        window.close()
    

    def pega_id_gato(self):
        layout = [
            [sg.Text("Digite o ID do gato que deseja buscar:")],
            [sg.InputText("", key="id")],
            [sg.Button("Buscar"), sg.Button("Cancelar")]
        ]

        self.window = sg.Window("Buscar gato", layout)

        while True:
            event, values = self.window.read()

            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                self.window.close()
                return None  # Se o usuário cancelar ou fechar a janela

            if event == "Buscar":
                try:
                    id_gato = int(values["id"])
                    self.window.close()
                    return id_gato  # Retorna o ID para buscar o gato
                except ValueError:
                    sg.popup("Por favor, insira um ID válido.")


    def pega_id_cachorro(self):
        layout = [
            [sg.Text("Digite o ID do cachorro selecionado:")],
            [sg.InputText("", key="id")],
            [sg.Button("Buscar"), sg.Button("Cancelar")]
        ]

        self.window = sg.Window("Buscar Cachorro", layout)

        while True:
            event, values = self.window.read()

            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                self.window.close()
                return None

            if event == "Buscar":
                try:
                    id_cachorro = int(values["id"])
                    self.window.close()
                    return id_cachorro  # Retorna o ID para buscar o cachorro
                except ValueError:
                    sg.popup("Por favor, insira um ID válido.")
    

    def gato_ou_cachorro(self):
        layout = [
            [sg.Button("Adotar Gato", key="adotar_gato",  size=(20, 1)), 
             sg.Button("Adotar Cachorro", key="adotar_cachorro",  size=(20, 1))
            ],
            [sg.Button("Cancelar")]
        ]

        window = sg.Window("Escolha entre Adotar Gato ou Cachorro", layout)

        while True:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None

            if event == "adotar_gato":
                window.close()
                return 1
            elif event == "adotar_cachorro":
                window.close()
                return 0
            
    
    def pega_dados_adocao(self):
        layout = [
            [sg.Text("Digite a data da Adoção (dd/mm/aaaa):"), sg.Input(key="data_adocao", size=(20, 1))],
            [sg.Text("Termo de responsabilidade. Concorda?"),  [sg.Radio("Sim", "CONCORDANCIA", key="-SIM-"), sg.Radio("Não", "CONCORDANCIA", key="-NAO-")],],
            [sg.Button("Salvar", key="salvar_adocao")],
            [sg.Button("Cancelar", key="cancelar_adocao")]
        ]
        window = sg.Window("Dados de Adoção", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "cancelar_adocao":
                window.close()
                return None  # Cancelado
            elif event == "salvar_adocao":
                try:
                    data_adocao = date(*map(int, values["data_adocao"].split('/')[::-1]))
                    termo = None

                    if values["-SIM-"]:
                        termo = True
                    elif values["-NAO-"]:
                        termo = False

                    if termo is not None:
                        window.close()
                        return {"data": data_adocao, "CONCORDANCIA": termo}
                    else:
                        sg.popup("Por favor, selecione 'Sim' ou 'Não' para o termo de responsabilidade.")

                except ValueError:
                    sg.popup("Data inválida. Por favor, insira no formato dd/mm/aaaa.")


    def erro(self, erro):
        sg.popup(erro)