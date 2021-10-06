from animacao import Animacao
import pygame
from tela import tela
from abc import ABC
from random import randint

# classe Abstrata

class Obstaculo(ABC):

    def __init__(self, posicao: list, velocidade: int, animacoes: list):
        self.__vivo = True
        self.__mostrar = True
        self.__posicao = posicao
        self.__aparecer_entre = (1228, 1500)
        self.__tempo_inicial_morto = None
        self.__velocidade = velocidade
        self.__animacoes = animacoes
        self.__animacao_atual = pygame.sprite.Group(self.__animacoes[0])
        self.__rect = self.__animacao_atual.sprites()[0].rect

    # Getters e setters

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def posicao(self):
        return self.__posicao

    @property
    def rect(self):
        return self.__rect

    @property
    def vivo(self):
        return self.__vivo

    @velocidade.setter
    def velocidade(self, nova):
        self.__velocidade = nova

    # troca a animacao

    def trocar_animacao(self, animacao_index: int):
        if self.__animacoes.index(self.__animacao_atual.sprites()[0]) != animacao_index:
            self.__animacao_atual = pygame.sprite.Group(
                self.__animacoes[animacao_index])

    # movimenta o obstaculo

    def movimento(self, dt, aparecer: int):
        self.__posicao[0] -= self.__velocidade * dt
        if self.__posicao[0] <= -80:
            self.__posicao[0] = aparecer

    # acompanha eventos do obstaculo

    def eventos(self):
        if self.__vivo is False and self.__animacao_atual.sprites()[0].atualizar is False:
            self.__mostrar = False

            if pygame.time.get_ticks() - self.__tempo_inicial_morto >= 500:
                self.__vivo = True
                self.__mostrar = True
                self.__animacao_atual.sprites()[0].atualizar = True
                self.__posicao[0] = -100
                self.trocar_animacao(0)

    # desenha o obstaculo

    def desenhar(self):
        self.__animacao_atual.sprites()[0].rect.topleft = self.posicao
        self.__rect = self.__animacao_atual.sprites()[0].rect

        if self.__mostrar:
            self.__animacao_atual.draw(tela.screen)

        self.__animacao_atual.update()

    # reseta a posicao, não "mata" de verdade

    def matar(self):
        self.__vivo = False
        self.__tempo_inicial_morto = pygame.time.get_ticks()
        self.trocar_animacao(1)

    # main loop

    def atualizar(self, dt):
        self.eventos()
        self.desenhar()
        self.movimento(dt, randint(
            self.__aparecer_entre[0], self.__aparecer_entre[1]))

# HERANÇA com especializaçao de Obstaculo

class Morcego(Obstaculo):

    def __init__(self, posicao: list, velocidade: int):
        super().__init__(posicao,
                         velocidade,
                         [Animacao((29, 17), 'versao_final/src/morcego/movimento/'),
                          Animacao((29, 17), 'versao_final/src/morcego/morte/', rodar_uma_vez=True)])

# HERANÇA com especializaçao de Obstaculo

class Golem(Obstaculo):

    def __init__(self, posicao: list, velocidade: int):
        super().__init__(posicao,
                         velocidade,
                         [Animacao((34, 38), 'versao_final/src/golem/movimento/'),
                          Animacao((34, 38), 'versao_final/src/golem/morte/', rodar_uma_vez=True)])
