from jogador import Jogador
from tela import Tela
from tela import tela
from animacao import EstaticoPoder
import pygame
import abc

# Classe base do poder

class Poder(abc.ABC):

    def __init__(self, diferencial: int, velocidade: float, posicao: list, sprite_path: str):
        self.__diferencial = diferencial
        self.__velocidade = velocidade
        self.__posicao = posicao
        self.__rect = pygame.Rect(self.__posicao[0], self.__posicao[1], 10, 10)
        self.__sprite = pygame.sprite.Group(
            EstaticoPoder(posicao, sprite_path))

    # getters

    @property
    def diferencial(self):
        return self.__diferencial

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def posicao(self):
        return self.__posicao

    @property
    def retangulo(self):
        return self.__rect

    # setters

    @velocidade.setter
    def velocidade(self, nova):
        self.__velocidade = nova

    @retangulo.setter
    def retangulo(self, novo):
        self.__rect = novo

    @abc.abstractmethod
    def usar(self, jogador: Jogador):
        pass

    # movimenta o poder

    def movimento(self, dt):
        self.__posicao[0] -= self.__velocidade * dt

    # desenha os poderes no chao

    def desenhar(self):
        self.__sprite.sprites()[0].rect.topleft = self.__posicao
        self.__rect = self.__sprite.sprites()[0].rect
        self.__sprite.draw(tela.screen)

    def atualizar(self, dt):
        self.desenhar()
        self.movimento(dt)

# Poder que aumenta 1 ponto de vida

class VidaPoder(Poder):

    def __init__(self, velocidade: float, posicao: list):
        super().__init__(diferencial=1,
                         velocidade=velocidade,
                         posicao=posicao,
                         sprite_path='versao_final/src/estaticos/pocao_vida.png')

    def usar(self, jogador: Jogador):
        if jogador.vida != jogador.vida_maxima:
            jogador.vida += self.diferencial

# poder q aumenta 1 ponto de stamina (+1 ataque de espada)

class StaminaPoder(Poder):

    def __init__(self, velocidade: float, posicao: list):
        super().__init__(diferencial=1,
                         velocidade=velocidade,
                         posicao=posicao,
                         sprite_path='versao_final/src/estaticos/pocao_stamina.png')

    def usar(self, jogador: Jogador):
        if jogador.stamina != jogador.stamina_maxima:
            jogador.stamina += self.diferencial

# Poder que deixa o jogador invulnerável por 3 segundos

class InvPoder(Poder):

    def __init__(self, velocidade: float, posicao: list):
        self.som_invencivel = pygame.mixer.Sound(
            'versao_final/src/efeitos_sonoros/invenc.mp3')
        super().__init__(diferencial=3000,
                         velocidade=velocidade,
                         posicao=posicao,
                         sprite_path='versao_final/src/estaticos/pocao_inv.png')

    # funçao que é chamado quando o jogador pega o poder, criando um som e chamando a funçao da invulnerabilidade

    def usar(self, jogador: Jogador):
        self.som_invencivel.play(3)
        jogador.tornar_invulneravel_por(self.diferencial)
