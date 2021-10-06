from personagem import Personagem
import pygame
from tela import tela
from constantes import Constantes
from animacao import Animacao

# HERANÇA de personagem com especializaçao

class Jogador(Personagem):

    def __init__(self):
        super().__init__(velocidade=400, posicao=[10, 420])
        self.constantes = Constantes()
        self.__animacoes = [Animacao((26, 29), 'versao_final/src/cavaleiro/movimento/'),
                            Animacao(
                                (26, 29), 'versao_final/src/cavaleiro/pulo/'),
                            Animacao((26, 29), 'versao_final/src/cavaleiro/ataque/', rodar_uma_vez=True)]

        self.__animacao_atual = pygame.sprite.Group(self.__animacoes[0])
        self.__tamanho_pulo = 55
        self.__velocidade_y = 10
        self.__pulando = False
        self.__atacando = False
        self.__ataque_rect = None
        self.__rect = self.__animacao_atual.sprites()[0].rect
        self.som_pulo = pygame.mixer.Sound(
            'versao_final/src/efeitos_sonoros/pulo.wav')
        self.som_ataque = pygame.mixer.Sound(
            'versao_final/src/efeitos_sonoros/golpe.wav')

    @property
    def rect(self):
        return self.__rect

    @property
    def ataque_rect(self):
        return self.__ataque_rect

    # movimento para a direita

    def movimento_direita(self, dt, seta_direita_pressionada):
        if seta_direita_pressionada:
            self.posicao[0] += self.velocidade * dt
            if self.posicao[0] > self.constantes.LIMITE_DIREITA:
                self.posicao[0] = self.constantes.LIMITE_DIREITA

    # movimento para a esquerda

    def movimento_esquerda(self, dt, seta_esquerda_pressionada):
        if seta_esquerda_pressionada:
            self.posicao[0] -= self.velocidade * dt
            if self.posicao[0] < self.constantes.LIMITE_ESQUERDA:
                self.posicao[0] = self.constantes.LIMITE_ESQUERDA

    # movimento do pulo

    def movimento_pulo(self, dt, seta_cima_pressionada):
        if self.__pulando is False and seta_cima_pressionada:
            self.__pulando = True
            self.som_pulo.play()

        if self.__pulando:
            self.trocar_animacao(1)
            self.posicao[1] -= self.__velocidade_y * \
                self.__tamanho_pulo * dt                              # tamanho do pulo
            self.__velocidade_y -= self.constantes.VELOCIDADE_QUEDA   # velocidade que o jogador cai

            # checa a colisão com o chão
            if self.posicao[1] >= self.constantes.LIMITE_CHAO:
                self.posicao[1] = self.constantes.LIMITE_CHAO
                self.__velocidade_y = self.constantes.VELOCIDADE
                self.__pulando = False

    # ataque do jogador

    def ataque(self, espaço):
        if espaço and not self.__atacando and not self.__pulando and not self.invulneravel and self.stamina > 0:
            self.stamina -= 1
            self.som_ataque.play()
            self.__atacando = True
            self.trocar_animacao(2)
            self.__ataque_rect = pygame.Rect(
                self.__rect.x+40, self.__rect.y, 50, 50)
            self.__animacao_atual.sprites()[0].atualizar = True

    # muda a animação atual se não for a mesma

    def trocar_animacao(self, animacao_index: int):
        if self.__animacoes.index(self.__animacao_atual.sprites()[0]) != animacao_index:
            self.__animacao_atual = pygame.sprite.Group(
                self.__animacoes[animacao_index])

    # eventos do jogador

    def eventos(self):

        # evento de invulnerabilidade
        if self.invulneravel:
            self.mostrar = not self.mostrar

            if pygame.time.get_ticks() - self.tempo_inicial_inv >= self.tempo_inv:
                self.invulneravel = False
                self.mostrar = True

        # evento de ataque
        if self.__atacando:
            self.__ataque_rect.x = self.__rect.x+40
            self.__ataque_rect.y = self.__rect.y

            if self.__animacao_atual.sprites()[0].atualizar is False:
                self.trocar_animacao(0)
                self.__atacando = False
                self.__ataque_rect = None

        # evento padrão (movendo)
        else:
            self.__atacando = False
            self.__ataque_rect = None
            self.trocar_animacao(0)

    # ações do usuario com o jogador

    def acoes(self, dt):
        botoes = pygame.key.get_pressed()
        self.ataque(botoes[pygame.K_SPACE])
        self.movimento_direita(dt, botoes[pygame.K_RIGHT])
        self.movimento_esquerda(dt, botoes[pygame.K_LEFT])
        self.movimento_pulo(dt, botoes[pygame.K_UP])

    # desenha o jogador

    def desenhar(self):
        self.__animacao_atual.sprites()[0].rect.topleft = self.posicao
        self.__rect = self.__animacao_atual.sprites()[0].rect

        if self.mostrar:
            self.__animacao_atual.draw(tela.screen)

        self.__animacao_atual.update()

    # Função de loop do jogador que entra no loop do jogo

    def atualizar(self, dt):
        self.acoes(dt)
        self.desenhar()
        self.eventos()
