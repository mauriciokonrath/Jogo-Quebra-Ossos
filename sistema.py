from jogo import Jogo
from tela import tela
from singleton import Singleton
from DAO.pontuacoesDAO import PontuacoesDAO
from state import State, Menu
import pygame
import sys
import time
import pygame
from pygame import mixer


# HERANÇA do Singleton
class Sistema(Singleton):

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(500, 100)
        pygame.mixer.init()
        self.__jogo = Jogo()                        # objeto do jogo
        self.__pontuacoes_dao = PontuacoesDAO()     # DAO das pontuacoes
        self.__ranking = {}                         # ranking das pontuacoes    
        self.__estado = None                        # estado da sistema (janela)
        self.__eventos = None                       # eventos de input do usuario
        self.__fundo_atual = None                   # atual fundo da janela
        self.__musica_atual = None                  # musica atual da janela
        self.__click = False                        # interação do usuário com a janela
        self.__clock = pygame.time.Clock()          # pygame clock
        self.__dt = 0                               # tempo de um frame (delta time)

    # main loop da janela

    def __main(self):
        tempo_inicial = time.time()

        while True:
            tempo_inicial = self.calcular_dt(tempo_inicial)
            self.__clock.tick(300)
            self.__estado.executar()

            self.track_eventos()
            self.atualizar_tela()

    # inicia o loop com o estado inicial sendo o menu

    def iniciar(self):
        self.__estado = Menu(self)
        self.__main()

    # recria o objeto do jogo

    def reiniciar_jogo(self):
        self.__jogo = Jogo()

    # salva o jogo atual

    def salvar(self, nome: str):
        self.__pontuacoes_dao.add(nome, self.__jogo.pontuacao)
        self.atualizar_ranking()

    # troca o atual estado por outro

    def proximo_estado(self, estado: State):
        self.__estado = estado

    # delta time é o tempo de um frame

    def calcular_dt(self, tempo_inicial):
        tempo_final = time.time()

        self.__dt = tempo_final - tempo_inicial
        return tempo_final

    # toca a musica atual, definida pelo estado

    def tocar_musica(self, loop=False):
        mixer.music.load(self.__musica_atual)

        if loop:
            mixer.music.play(-1)

        else:
            mixer.music.play()

    # Atualiza as posiçoes do ranking organizando do maior para o menor

    def atualizar_ranking(self):
        def ordenar_ranking(item): return item[1]
        self.__ranking = self.__pontuacoes_dao.get_all()
        self.__ranking = sorted(
            self.__ranking, key=ordenar_ranking, reverse=True)

    # registra eventos de input do usuário

    def track_eventos(self):
        self.__eventos = pygame.event.get()
        for event in self.__eventos:

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.__click = True

            else:
                self.__click = False

    # desenha o fundo atual, definido pelo estado

    def desenhar_fundo(self):
        tela.screen.blit(self.__fundo_atual, self.__fundo_atual.get_rect())

    # atualiza o display da janela

    def atualizar_tela(self):
        pygame.display.update()
        tela.screen.fill((0, 0, 0))

    # getters

    @property
    def estado(self):
        return self.__estado

    @property
    def eventos(self):
        return self.__eventos

    @property
    def jogo(self):
        return self.__jogo

    @property
    def click(self):
        return self.__click

    @property
    def dt(self):
        return self.__dt

    @property
    def fundo_atual(self):
        return self.__fundo_atual

    @property
    def musica_atual(self):
        return self.__musica_atual

    @property
    def ranking(self):
        return self.__ranking

    # setters
   
    @ranking.setter
    def ranking(self, ranking):
        self.__ranking = ranking

    @fundo_atual.setter
    def fundo_atual(self, fundo):
        self.__fundo_atual = fundo

    @musica_atual.setter
    def musica_atual(self, musica):
        self.__musica_atual = musica
