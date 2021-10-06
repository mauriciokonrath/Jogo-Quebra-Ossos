import pygame
import abc
import os
from copy import copy
from pygame import constants
from constantes import Constantes


class Animacao(pygame.sprite.Sprite):

    def __init__(self, dimensao, path, velocidade=0.03, rodar_uma_vez=False):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        try:
            self.__carregar_sprites(path)
        except FileNotFoundError as e:
            print(e)

        self.sprite_atual_index = 0
        self.velocidade_troca_sprite = velocidade
        self.rodar_uma_vez = rodar_uma_vez
        self.atualizar = True
        self.sprite_atual = self.sprites[self.sprite_atual_index]
        self.rect = self.sprite_atual.get_rect()
        self.dimensao = dimensao
        self.sprite_atual = pygame.transform.scale(
            self.sprite_atual, (dimensao[0]*2, dimensao[1]*2))
        self.image = self.sprite_atual

    # carrega as sprites

    def __carregar_sprites(self, path):
        for nome_sprite in os.listdir(path):
            self.sprites.append(pygame.image.load(path + nome_sprite))

    # processa o sprite atual, alterando a escala, o rect e a image do pygame.sprite.Sprite

    def processar_sprite(self):
        self.sprite_atual = pygame.transform.scale(
            self.sprite_atual, (self.dimensao[0]*2, self.dimensao[1]*2))
        self.rect = self.sprite_atual.get_rect()
        self.image = self.sprite_atual

    # troca de sprite com base na velocidade

    def update(self):
        if self.atualizar:
            self.sprite_atual_index += self.velocidade_troca_sprite

            if self.sprite_atual_index >= len(self.sprites):
                self.sprite_atual_index = 0

                if self.rodar_uma_vez:
                    self.atualizar = False

            self.sprite_atual = self.sprites[int(self.sprite_atual_index) - 1]
            self.processar_sprite()

# Classe de sprites que nao possuem alteração de imagens (sem animação, só uma imagem)

class Estatico(pygame.sprite.Sprite):

    def __init__(self, posicao, sprite_path, dimensao=None, escala=2, escalar=False):
        pygame.sprite.Sprite.__init__(self)
        self.posicao = posicao
        self.imagem = pygame.image.load(sprite_path)

        if escalar:
            self.imagem = pygame.transform.scale(
                self.imagem, (dimensao[0]*escala, dimensao[1]*escala))

        self.image = self.imagem
        self.rect = self.imagem.get_rect()
        self.rect.topleft = [self.posicao[0], self.posicao[1]]

# HERANÇA de Animacao com especializacao

class EstaticoFundo(Estatico):

    def __init__(self, posicao: list, path: str):
        super().__init__(posicao, path)

# HERANÇA de Estatico com especializaçao das sprites de quantidade de vida

class EstaticoCoracao(Estatico):

    def __init__(self, posicao):
        super().__init__(posicao,
                         'versao_final/src/estaticos/coracao.png',
                         (17, 17),
                         escalar=True)

# Sprite da barra de stamina

class EstaticoBarraStamina(Estatico):

    def __init__(self, posicao, path):
        super().__init__(posicao,
                         path,
                         (67, 29),
                         escalar=True)

# HERANÇA de Estatico especializaçao das sprites dos poderes (poçoes)

class EstaticoPoder(Estatico):

    def __init__(self, posicao, path):
        super().__init__(posicao,
                         path,
                         (17, 17),
                         escalar=True)
