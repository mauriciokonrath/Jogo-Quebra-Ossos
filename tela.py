import pygame
from singleton import Singleton


class Tela(Singleton):

    # resolução da tela
    def __init__(self, display=(928, 600)):
        super().__init__()
        self.display = display
        pygame.display.set_caption("Quebra Ossos")

        logo = pygame.image.load('versao_final/src/logo/logo.png')
        pygame.display.set_icon(logo)

        # setup da janela
        self.screen = pygame.display.set_mode(display)


tela = Tela()
