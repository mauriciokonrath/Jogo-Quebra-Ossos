from tela import tela
from poder import InvPoder, VidaPoder, StaminaPoder
from random import choice
from animacao import EstaticoCoracao, EstaticoBarraStamina, EstaticoFundo
import pygame


class Cenario:

    def __init__(self, obstaculos: list):
        self.__obstaculos = obstaculos      # lista de obstaculos
        self.__poder_na_tela = None         # atual poder na tela
        self.__tempo_invocado = 0           # o tempo em que o ultimo poder foi invocado
        self.__velocidade_acumulada = 0     # velocidade acumulada da aceleração do cenário
        self.__aceleracao = 0.5
        self.__coracoes = [pygame.sprite.Group(coracao) for coracao in [EstaticoCoracao([800, 24]),
                                                                        EstaticoCoracao(
                                                                            [840, 24]),
                                                                        EstaticoCoracao([880, 24])]]

        self.__barras_stamina = [pygame.sprite.Group(barra) for barra in [EstaticoBarraStamina([650, 10], 'versao_final/src/stamina/stamina_0.png'),
                                                                          EstaticoBarraStamina(
                                                                              [650, 10], 'versao_final/src/stamina/stamina_1.png'),
                                                                          EstaticoBarraStamina(
                                                                              [650, 10], 'versao_final/src/stamina/stamina_2.png'),
                                                                          EstaticoBarraStamina([650, 10], 'versao_final/src/stamina/stamina_3.png')]]

        self.__posicao_fundo = [0, 0]
        self.__posicao_fundo_inv = [928, 0]
        self.__fundos = pygame.sprite.Group(EstaticoFundo(self.__posicao_fundo, 'versao_final/src/backgrounds/fundo_jogo.jpg'),
                                            EstaticoFundo(self.__posicao_fundo_inv, 'versao_final/src/backgrounds/fundo_jogo_inv.jpg'))

    # Getters e setters

    @property
    def coracoes(self):
        return self.__coracoes

    @property
    def barras_stamina(self):
        return self.__barras_stamina

    @property
    def obstaculos(self):
        return self.__obstaculos

    @property
    def poder_na_tela(self):
        return self.__poder_na_tela

    @poder_na_tela.setter
    def poder_na_tela(self, novo):
        self.__poder_na_tela = novo

    # invoca poderes na tela

    def invocador(self, dt):
        if pygame.time.get_ticks() - self.__tempo_invocado >= 5000:
            self.__poder_na_tela = choice([InvPoder(300+self.__velocidade_acumulada, [1328, 424]),
                                           VidaPoder(
                                               300+self.__velocidade_acumulada, [1328, 424]),
                                           StaminaPoder(300+self.__velocidade_acumulada, [1328, 424])])

            self.__tempo_invocado = pygame.time.get_ticks()

        # se tiver algum poder na tela ele atualiza para o movimento seguir o chao
        if self.__poder_na_tela != None:
            self.__poder_na_tela.atualizar(dt)

    # acelera todos os objetos do cenário até um certo valor (obstáculos e poderes)

    def acelerar(self):
        if self.__velocidade_acumulada < 200:
            if self.obstaculos[0].posicao[0] <= -39:
                for obs in self.__obstaculos:
                    obs.velocidade += self.__aceleracao
                self.__velocidade_acumulada += self.__aceleracao

                if self.poder_na_tela != None:
                    self.__poder_na_tela.velocidade += self.__aceleracao

    # funçao que movimenta o cenario

    def mover_cenario(self, dt):
        self.__posicao_fundo[0] -= (1 + self.__velocidade_acumulada*dt/3)
        self.__posicao_fundo_inv[0] -= (1 + self.__velocidade_acumulada*dt/3)

        for fundo, posicao in zip(self.__fundos.sprites(), [self.__posicao_fundo, self.__posicao_fundo_inv]):
            if posicao[0] <= -928:
                posicao[0] = 928

            fundo.rect.topleft = posicao

    # desenha o chão do jogo

    def desenhar(self):
        self.__fundos.draw(tela.screen)
        self.__fundos.update()

    # atualiza os obstáculos

    def atualizar(self, dt):
        self.desenhar()
        self.acelerar()
        self.mover_cenario(dt)
        self.invocador(dt)

        for obs in self.__obstaculos:
            obs.atualizar(dt)
