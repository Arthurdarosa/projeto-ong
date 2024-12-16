import PySimpleGUI as sg
from datetime import date


class TelaSistema:

    def tela_opcoes(self):
        sg.theme('LightBlue')
        layout = [
            [sg.Text("----Sistema ONG----", font=("Helvetica", 16))],
            [sg.Button("Adotar", key="adotar", size=(20, 1))],
            [sg.Button("Doar", key="doar", size=(20, 1))],
            [sg.Text("----Cadastro dos Animais----", font=("Helvetica", 16))],
            [],
            [sg.Button("cachorro", key="cachorro", size=(10, 1)), sg.Button("gato", key="gato", size=(10, 1))],
            [sg.Button("Relatórios", key="relatorios", size=(20, 1))],
            [sg.Button("Finalizar", key="finalizar", size=(20, 1))]
        ]
        window = sg.Window("Sistema ONG", layout)

        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "finalizar"):
                window.close()
                return 0  # Finalizar
            elif event == "adotar":
                window.close()
                return 1  # Adotar
            elif event == "doar":
                window.close()
                return 2  # Doar
            elif event == "cachorro":
                window.close()
                return 5
            elif event == "gato":
                window.close()
                return 6
            elif event == "relatorios":
                window.close()
                return 4  # Relatórios


    def opcao_relatorios(self):
        layout = [
            [sg.Text("----Relatórios----", font=("Helvetica", 16))],
            [sg.Button("Relatório Adoções", key="relatorio_adocoes")],
            [sg.Button("Relatório Doações", key="relatorio_doacoes")],
            [sg.Button("Animais Disponíveis", key="animais_disponiveis")],
            [sg.Button("Retornar", key="retornar_relatorio")]
        ]
        window = sg.Window("Relatórios", layout)

        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == "retornar_relatorio":
                window.close()
                return 0  # Retornar
            elif event == "relatorio_adocoes":
                window.close()
                return 1  # Relatório de Adoções
            elif event == "relatorio_doacoes":
                window.close()
                return 2  # Relatório de Doações
            elif event == "animais_disponiveis":
                window.close()
                return 3  # Animais Disponíveis

    def exibir_relatorio(self, texto):
        layout = [
            [sg.Text("Relatório:", font=("Helvetica", 16))],
            [sg.Multiline(texto, size=(80, 20), disabled=True, key="-RELATORIO-")],
            [sg.Button("Voltar", key="voltar")]
        ]
        window = sg.Window("Relatório", layout)

        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == "voltar":
                window.close()
                break


    def datas_filtro(self):
        layout = [
            [sg.Text("----Relatórios----", font=("Helvetica", 16))],
            [sg.Button("Todos os Registros", key="todos_registros")],
            [sg.Button("Buscar por Período", key="buscar_periodo")],
            [sg.Button("Cancelar", key="cancelar_filtro")]
        ]
        window = sg.Window("Filtro de Relatórios", layout)

        while True:
            event, _ = window.read()
            if event == sg.WIN_CLOSED or event == "cancelar_filtro":
                window.close()
                return 1  # Todos relatórios
            elif event == "todos_registros":
                window.close()
                return 1  # Todos relatórios
            elif event == "buscar_periodo":
                window.close()
                layout_periodo = [
                    [sg.Text("Digite a data de início (dd/mm/aaaa):"), sg.Input(key="inicio", size=(20, 1))],
                    [sg.Text("Digite a data de fim (dd/mm/aaaa):"), sg.Input(key="fim", size=(20, 1))],
                    [sg.Button("Confirmar", key="confirmar_periodo")],
                    [sg.Button("Cancelar", key="cancelar_periodo")]
                ]
                window_periodo = sg.Window("Buscar por Período", layout_periodo)

                while True:
                    event_periodo, values_periodo = window_periodo.read()
                    if event_periodo == sg.WIN_CLOSED or event_periodo == "cancelar_periodo":
                        window_periodo.close()
                        return None
                    elif event_periodo == "confirmar_periodo":
                        try:
                            data_inicio = date(*map(int, values_periodo["inicio"].split('/')[::-1]))
                            data_fim = date(*map(int, values_periodo["fim"].split('/')[::-1]))
                            window_periodo.close()
                            return {"inicio": data_inicio, "fim": data_fim}
                        except ValueError:
                            sg.popup("Data inválida. Por favor, insira no formato dd/mm/aaaa.")


    def erro(self, erro):
        sg.popup(erro)
