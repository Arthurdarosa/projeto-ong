import PySimpleGUI as sg
from datetime import date
from entidade.vacinacao import Vacinacao
from exceptions.IdNotFound import *


class TelaCachorro:

    def tela_opcoes(self):
        layout = [
            [sg.Text("----Cachorro----")],
            [sg.Button("Cadastrar Cachorro"), sg.Button("Gerenciar Cachorros"), sg.Button("Ver Histórico de Vacinação")],
            [sg.Button("Retornar")]
        ]

        window = sg.Window("Opções de Cachorro", layout)

        while True:
            event, _ = window.read()

            if event in (None, "Retornar"):
                window.close()
                return 0
            elif event == "Cadastrar Cachorro":
                window.close()
                return 1
            elif event == "Gerenciar Cachorros":
                window.close()
                return 2
            elif event == "Ver Histórico de Vacinação":
                window.close()
                return 3


    def pega_dados_cachorro(self, modo = "cadastro", dados_existentes = None):
        id_disabled = (modo == "alteracao")

        layout = [
            [sg.Text("-------- DADOS CACHORRO ----------")],
            [sg.Text("ID (número inteiro):"), sg.InputText(
            dados_existentes if dados_existentes else "",
            key="id", disabled=id_disabled
            )],
            [sg.Text("Nome:"), sg.InputText("", key="nome")],
            [sg.Text("Raça:"), sg.InputText("", key="raca")],
            [
                sg.Text("Porte:"),
                sg.Combo(["1 - Pequeno", "2 - Médio", "3 - Grande"], key="porte", readonly=True),
            ],
            [sg.Text("Vacinas disponíveis:")],
            [
                sg.Checkbox("1 - Raiva", key="vacina_1"),
                sg.InputText("", size=(10, 1), key="data_vacina_1", tooltip="Data de vacinação (dd/mm/aaaa)"),
            ],
            [
                sg.Checkbox("2 - Leptospirose", key="vacina_2"),
                sg.InputText("", size=(10, 1), key="data_vacina_2", tooltip="Data de vacinação (dd/mm/aaaa)"),
            ],
            [
                sg.Checkbox("3 - Hepatite", key="vacina_3"),
                sg.InputText("", size=(10, 1), key="data_vacina_3", tooltip="Data de vacinação (dd/mm/aaaa)"),
            ],
            [sg.Button("Finalizar")],[sg.Button("Cancelar")],
        ]

        window = sg.Window("Cadastro de Cachorro", layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                window.close()
                break

            if event == "Cancelar":
                window.close()
                break

            if event == "Finalizar":
                try:
                    vacinas = {}

                    for i in range(1, 4):
                        if values[f"vacina_{i}"]:
                            data_vacina = values[f"data_vacina_{i}"]
                            partes_data = data_vacina.split('/')
                            if len(partes_data) == 3:
                                dia, mes, ano = map(int, partes_data)
                                data_vacina_obj = date(ano, mes, dia)
                                vacinas[i] = data_vacina_obj
                            else:
                                sg.popup(f"Formato de data inválido para a vacina {i}. Por favor, insira no formato dd/mm/aaaa.")
                                raise ValueError("Data inválida")

                    porte_selecionado = values["porte"]
                    if porte_selecionado:
                        porte_inteiro = int(porte_selecionado.split(" - ")[0])
                    else:
                        raise ValueError("Por favor, selecione um porte válido.")

                    window.close()

                    # Retornar os dados coletados
                    return {
                        "id": int(values["id"]),
                        "nome": values["nome"],
                        "raca": values["raca"],
                        "porte": porte_inteiro,
                        "vacinas": list(vacinas.keys()),
                        "datas_vacinas": list(vacinas.values()),
                    }
                except Exception as e:
                    sg.popup(f"Erro ao finalizar: {e}")


    def janela_opcoes(self, cachorro):
        layout = [
            [sg.Text(f"Você escolheu {cachorro['nome']}.")],
            [sg.Text(f"ID: {cachorro['id']}")],
            [sg.Text(f"Raça: {cachorro['raca']}")],
            [sg.Text(f"Porte: {cachorro['porte']}")],
            [sg.Text(f"Vacinas: {cachorro['vacinas']}")],
            [sg.Button("Alterar"), sg.Button("Excluir"),sg.Button("Cancelar")],
        ]
        window = sg.Window(f"Cachorro selecionado: {cachorro['nome']}", layout, modal=True)

        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                window.close()
                return None  # Nenhuma ação
            elif event == "Alterar":
                window.close()
                return ("alterar", cachorro["id"])
            elif event == "Excluir":
                window.close()
                return ("excluir", cachorro["id"])


    def mostra_cachorro(self, cachorros):
        layout = [
            [sg.Text("Lista de Cachorros Cadastrados:")],
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
                    acao = self.janela_opcoes(cachorro)
                    if acao:
                        window.close()
                        return acao
            elif event == "Buscar por ID":
                try:
                    id_cachorro = self.pega_id()
                    cachorro = next(c for c in cachorros if c["id"] == id_cachorro)
                    acao = self.janela_opcoes(cachorro)
                    if acao:
                        window.close()
                        return acao
                except ValueError:
                    self.erro("ID inválido! Por favor, insira um número válido.")
                except StopIteration:
                    self.erro(idnotfound(id_cachorro))
                     

        window.close()


    def exibir_vacinas(self, texto):
        
        layout = [
            [sg.Text("vacinas:", font=("Helvetica", 16))],
            [sg.Multiline(texto, size=(80, 20), disabled=True, key="-vacinas-")],
            [sg.Button("Voltar", key="voltar")]
        ]
        window = sg.Window("historico de vacinas", layout)

        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == "voltar":
                window.close()
                break        


    def pega_id(self):
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
                return None  # Se o usuário cancelar ou fechar a janela

            if event == "Buscar":
                try:
                    id_cachorro = int(values["id"])
                    self.window.close()
                    return id_cachorro  # Retorna o ID para buscar o cachorro
                except ValueError:
                    sg.popup("Por favor, insira um ID válido.")


    def erro(self, erro):
        sg.popup(erro)