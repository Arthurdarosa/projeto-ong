from limite.tela_sistema import TelaSistema
from entidade.cachorro import Cachorro
from entidade.gato import Gato
from entidade.doador import Doador
from controle.controlador_cachorro import ControladorCachorro
from controle.controlador_adotante import Controladoradotante
from controle.controlador_doador import Controladordoador
from controle.controlador_gato import ControladorGato
from controle.controlador_doacao import ControladorDoacao
from controle.controlador_adocao import ControladorAdocao
from eventdispatcher import EventDispatcher
from DAOs.doacao_dao import DoacaoDAO
from DAOs.adocao_dao import AdocaoDAO
from DAOs.cachorro_dao import CachorroDAO
from DAOs.gato_dao import GatoDAO
from DAOs.doador_dao import DoadorDAO

class ControladorSistema():

    def __init__(self):
        self.__event_dispatcher = EventDispatcher()
        self.__controlador_gato = ControladorGato(self)
        self.__controlador_doador = Controladordoador(self)
        self.__controlador_adotante = Controladoradotante(self)
        self.__controlador_cachorro = ControladorCachorro(self)
        self.__controlador_doacao = ControladorDoacao(self)
        self.__controlador_adocao = ControladorAdocao(self)
        self.__tela_sistema = TelaSistema()
        self.__doacao_DAO = DoacaoDAO()
        self.__adocao_DAO = AdocaoDAO()
        self.__cachorro_DAO = CachorroDAO()
        self.__gato_DAO = GatoDAO()
        self.__doador_DAO = DoadorDAO()
    
        self.__event_dispatcher.register("doador_cadastrado_cachorro", self.cadastrar_cachorro_doadado)
        self.__event_dispatcher.register("doador_cadastrado_gato", self.cadastrar_gato_doadado)
        self.__event_dispatcher.register("adotante_ja_cadastrado", self.adocao)

    @property
    def controlador_cachorro(self):
        return self.__controlador_cachorro

    @property
    def controlador_gato(self):
        return self.__controlador_gato

    @property
    def tela_sistema(self):
        return self.__tela_sistema

    def cadastrar_cachorro_doadado(self, doador):
        cachorro = self.__controlador_doacao.cadastrar_doacao_com_cachorro(doador)
        if cachorro is None:
            self.__tela_sistema.erro("Erro ao doar cachorro")
        else:
            self.__tela_sistema.erro(f"Cachorro {cachorro.nome} doado com sucesso pelo doador {doador.nome}!")
    

    def cadastrar_gato_doadado(self, doador):
        gato = self.__controlador_doacao.cadastrar_doacao_com_gato(doador)
        if gato is None:
            self.__tela_sistema.erro("Erro ao doar gato")
        else:
            self.__tela_sistema.erro(f"Cachorro {gato.nome} doado com sucesso pelo doador {doador.nome}!")


    def adocao(self, adotante):

        animais_formatados = []
        for cachorro in self.__cachorro_DAO.get_all():
            vacinas = ", ".join([f"{v.tipo_vacina.name} (Data: {v.dia_vacina.strftime('%d/%m/%Y')})" for v in cachorro.vacinas]) if cachorro.vacinas else "Nenhuma vacina"
            animais_formatados.append({
                "id": cachorro.id, "nome": cachorro.nome, "raca": cachorro.raca,
                "porte": cachorro.porte.name, "vacinas": vacinas
            })

        for gato in self.__gato_DAO.get_all():
            vacinas = ", ".join([f"{v.tipo_vacina.name} (Data: {v.dia_vacina.strftime('%d/%m/%Y')})" for v in gato.vacinas]) if gato.vacinas else "Nenhuma vacina"
            animais_formatados.append({
                "id": gato.id, "nome": gato.nome, "raca": gato.raca, 
                "vacinas": vacinas
            })

        animais_disponiveis = self.__controlador_adocao.filtrar_animais(animais_formatados)
        conferir_se_doador = self.buscar_doador_por_cpf(adotante.cpf)

        if not animais_disponiveis:
            self.__tela_sistema.erro("Não há animais disponíveis para adoção")
        elif conferir_se_doador:
            self.__controlador_adocao.adotar(animais_disponiveis, adotante)
        else:
            self.__tela_sistema.erro("Doadores não podem adotar novos animais")


    def animais_disponiveis(self):
        disponiveis = []
        
        for cachorro in self.__controlador_cachorro._ControladorCachorro__cachorro_DAO.get_all():
            if len(cachorro.vacinas) >= 3:
                disponiveis.append(cachorro)

        for gato in self.__controlador_gato._ControladorGato__gato_DAO.get_all():
            if len(gato.vacinas) >= 3:
                disponiveis.append(gato)

        return disponiveis


    def buscar_animal_por_id(self, id):
        for animal in self.animais_disponiveis():
            if animal.id == id:
                return animal
        return None
    

    def buscar_doador_por_cpf(self, cpf):
        doador = self.__doador_DAO.get(cpf)
        if isinstance(doador, Doador):
            return False
        return True


    def dispatch_event(self, event_type, *args, **kwargs):
        self.__event_dispatcher.dispatch(event_type, *args, **kwargs)


    def relatorios(self):
        opcao = self.__tela_sistema.opcao_relatorios()

        if opcao == 0:
            return

        elif opcao == 1:
            adocoes = self.__adocao_DAO.get_all()
            if not adocoes:
                relatorio = "Não há adoções registradas."
            else:
                adocoes_filtradas = self.filtrar_por_data(adocoes, "data_de_adocao")
                if not adocoes_filtradas:
                    return

                relatorio = "---- Relatório de Adoções ----\n"
                for item in adocoes_filtradas:
                    cachorro_ou_gato = "G-" if isinstance(item.animal, Gato) else "C-"
                    relatorio += (
                        f"Data: {item.data_de_adocao.strftime('%d/%m/%Y')}, "
                        f"ID Animal: {cachorro_ou_gato}{item.animal.id}, "
                        f"CPF Adotante: {item.adotante.cpf}, "
                        f"Termo: {item.termo_responsabilidade}\n"
                    )
            self.__tela_sistema.exibir_relatorio(relatorio)

        elif opcao == 2:
            doacoes = self.__doacao_DAO.get_all()
            if not doacoes:
                relatorio = "Não há doações registradas."
            else:
                doacoes_filtradas = self.filtrar_por_data(doacoes, "data_de_doacao")
                if not doacoes_filtradas:
                    return

                relatorio = "---- Relatório de Doações ----\n"
                for item in doacoes_filtradas:
                    cachorro_ou_gato = "G-" if isinstance(item.animal, Gato) else "C-"
                    relatorio += (
                        f"Data: {item.data_de_doacao.strftime('%d/%m/%Y')}, "
                        f"Motivo: {item.motivo}, "
                        f"CPF Doador: {item.doador.cpf}, "
                        f"ID Animal: {cachorro_ou_gato}{item.animal.id}\n"
                    )
            self.__tela_sistema.exibir_relatorio(relatorio)

        elif opcao == 3:
            animais = self.animais_disponiveis()
            if not animais:
                relatorio = "Nenhum animal disponível para adoção no momento."
            else:
                relatorio = "---- Animais Disponíveis ----\n"
                for animal in animais:
                    if isinstance(animal, Cachorro):
                        relatorio += (
                            f"Animal: Cachorro, ID: {animal.id}, Nome: {animal.nome}, "
                            f"Raça: {animal.raca}, Porte: {animal.porte.name}\n"
                        )
                    elif isinstance(animal, Gato):
                        relatorio += (
                            f"Animal: Gato, ID: {animal.id}, Nome: {animal.nome}, "
                            f"Raça: {animal.raca}\n"
                        )
            self.__tela_sistema.exibir_relatorio(relatorio)



    def filtrar_por_data(self, registros, atributo_data):
        datas_dict = self.__tela_sistema.datas_filtro()

        if datas_dict == 1 or not datas_dict:
            return registros

        data_inicio = datas_dict["inicio"]
        data_fim = datas_dict["fim"]

        registros_filtrados = [
            registro
            for registro in registros
            if data_inicio <= getattr(registro, atributo_data) <= data_fim
        ]

        if registros_filtrados:
            return registros_filtrados
        else:
            self.__tela_sistema.erro(f"Não há registros entre {data_inicio} e {data_fim}.")
            return []

    def inicializa_sistema(self):
        self.abre_tela()
    
    def cadastra_cachorro(self):
        self.__controlador_cachorro.abre_tela()

    def cadastra_gato(self):
        self.__controlador_gato.abre_tela()

    def cadastra_doador(self):
        self.__controlador_doador.abre_tela()

    def cadastra_adotante(self):
        self.__controlador_adotante.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1:self.cadastra_adotante,2: self.cadastra_doador, 4: self.relatorios,5: self.cadastra_cachorro,6: self.cadastra_gato, 0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()