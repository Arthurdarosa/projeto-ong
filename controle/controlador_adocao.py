from entidade.adocao import Adocao
from entidade.cachorro import Cachorro
from entidade.tipo_moradia import TipoMoradia, TamanhoMoradia
from entidade.gato import Gato
from limite.tela_adocao import TelaAdocao
from DAOs.adocao_dao import AdocaoDAO

class ControladorAdocao:

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_adocao = TelaAdocao()
        self.__adocao_DAO = AdocaoDAO()
    

    def filtrar_animais(self, animais):
        animais_disponiveis = []
        for i in animais:
            vacinas = i["vacinas"]

            if vacinas != "Nenhuma vacina" and vacinas.count(", ") >= 2:
                animais_disponiveis.append(i)
            else:
                pass
        return animais_disponiveis
    
    def adotar(self, animais, adotante):
        controlador_cachorro = self.__controlador_sistema.controlador_cachorro
        controlador_gato = self.__controlador_sistema.controlador_gato

        cachorros = [d for d in animais if len(d) == 5]
        gatos = [d for d in animais if len(d) == 4]

        gato_ou_cachorro = self.__tela_adocao.gato_ou_cachorro()
        if gato_ou_cachorro == 1:
            if gatos:
                id_gato = self.__tela_adocao.mostra_gato(gatos)
                animal_escolhido = controlador_gato.buscar_gato_por_id(id_gato)
            else:
                self.__tela_adocao.erro("Nenhum Gato disponível para adoção")
                return

        elif gato_ou_cachorro == 0:
            if cachorros:
                id_cachorro = self.__tela_adocao.mostra_cachorro(cachorros)
                animal_escolhido = controlador_cachorro.buscar_cachorro_por_id(id_cachorro)
            else:
                self.__tela_adocao.erro("Nenhum Cachorro disponível para adoção")
                return

        tipo_moradia, tamanho_moradia = adotante.tipo_moradia
        if isinstance(animal_escolhido, Cachorro):
            if animal_escolhido.porte.name == "GRANDE" and tipo_moradia == TipoMoradia.APARTAMENTO and tamanho_moradia == TamanhoMoradia.PEQUENO:
                self.__tela_adocao.erro("Cães de porte grande não podem ser adotados por pessoas que moram em apartamento pequeno. ")
                return
        
        dados_adocao = self.__tela_adocao.pega_dados_adocao()
        if dados_adocao == None:
            self.__tela_adocao.erro("Adoção não pode ser concluída sem a assinatura do Termo de Responsabilidade. ")
            return
        if dados_adocao["CONCORDANCIA"] == False:
            self.__tela_adocao.erro("Adoção não pode ser concluída sem a assinatura do Termo de Responsabilidade. ")
            return

        adocao = Adocao(dados_adocao["data"], animal_escolhido, adotante, dados_adocao["CONCORDANCIA"])
        if isinstance(adocao, Adocao):
            self.__adocao_DAO.add(adocao)
            self.__tela_adocao.erro(f"Animal {animal_escolhido.nome} adotado com sucesso por {adotante.nome}!")
        

            if isinstance(animal_escolhido, Cachorro):
                controlador_cachorro.excluir_cachorro(animal_escolhido.id, modo = "adotado")
            else:
                controlador_gato.excluir_gato(animal_escolhido.id, modo = "adotado")
            return
        else:
            self.__tela_adocao.erro("erro ao instanciar doacao")