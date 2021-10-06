from singleton import Singleton
import pygame

# constantes globais

class Constantes(Singleton):

    def __init__(self):
        super().__init__()
        self.LIMITE_ESQUERDA = 0
        self.LIMITE_DIREITA = 908
        self.LIMITE_CHAO = 420
        self.VELOCIDADE_QUEDA = 0.06
        self.VELOCIDADE = 10
