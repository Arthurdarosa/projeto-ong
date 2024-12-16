import PySimpleGUI as sg
from datetime import date

class TelaDoacao:

    def pega_dados_doacao(self):
        layout = [
            [sg.Text("Digite a data da Doação (dd/mm/aaaa):"), sg.Input(key="data_doacao", size=(20, 1))],
            [sg.Text("Motivo da Doação:"), sg.Input(key="motivo", size=(40, 1))],
            [sg.Button("Salvar", key="salvar_doacao")],
            [sg.Button("Cancelar", key="cancelar_doacao")]
        ]
        window = sg.Window("Dados de Doação", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "cancelar_doacao":
                window.close()
                return None  # Cancelado
            elif event == "salvar_doacao":
                try:
                    validar = values["data_doacao"].split('/')[::-1]
                    if len(validar) != 3:
                        raise ValueError("Formato de data inválido. Use dd/mm/yyyy.")

                    data_doacao = date(*map(int, values["data_doacao"].split('/')[::-1]))
                    motivo = values["motivo"].strip()
                    if motivo:
                        window.close()
                        return {"data": data_doacao, "motivo": motivo}
                    else:
                        sg.popup("Motivo não pode estar em branco.")
                except ValueError:
                    sg.popup("Data inválida. Por favor, insira no formato dd/mm/aaaa.")