from abc import ABC, abstractmethod
from tela import tela
import pygame
import sys
from nome_vazioException import NomeVazio
from maior15_Exception import Maior15_Caracteres

# Classe Abstrata

class State(ABC):

    def __init__(self, sistema, fundo, musica):
        self._sistema = sistema
        self._efeito_sonoro = pygame.mixer.Sound(
            'versao_final/src/efeitos_sonoros/espada2.mp3')
        self.__setup(fundo, musica)

    def __setup(self, fundo, musica):
        try:
            self._sistema.fundo_atual = pygame.image.load(fundo)

        except TypeError:
            self._sistema.fundo_atual = None

        self._sistema.musica_atual = musica

    # getters e setters

    @property
    def sistema(self):
        return self._sistema

    @property
    def efeito_sonoro(self):
        return self._efeito_sonoro

    @sistema.setter
    def sistema(self, sistema):
        self._sistema = sistema

    @abstractmethod
    def executar(self):
        pass

# HERANÇA de State executada até receber um evento de click em algum dos botoes

class Menu(State):

    def __init__(self, sistema,
                 fundo="versao_final/src/backgrounds/tela_inicial.png",
                 musica='versao_final/src/musicas/menu.mp3'):

        super().__init__(sistema, fundo, musica)
        self.sistema.tocar_musica(loop=True)
        self.button_jogar = pygame.Rect(40, 180, 374, 94)
        self.button_ranking = pygame.Rect(40, 280, 374, 94)
        self.button_sair = pygame.Rect(40, 380, 374, 94)

    # Executa uma tela com todas as opçoes do jogo antes de inicialo (menu)

    def executar(self):
        self.sistema.desenhar_fundo()
        mx, my = pygame.mouse.get_pos()
        proximo_estado = None

        # mapeia o click na tela para mudar a tela de acordo com o botao clicado

        if self.sistema.click:
            for bttn in [self.button_jogar, self.button_ranking, self.button_sair]:
                if bttn.collidepoint((mx, my)):
                    self.efeito_sonoro.play()
                    if bttn == self.button_jogar:
                        proximo_estado = Jogando(self.sistema)
                    elif bttn == self.button_ranking:
                        proximo_estado = Ranking(self.sistema)
                    elif bttn == self.button_sair:
                        sys.exit()

        # passa para o proximo estado

        if proximo_estado != None:
            self.sistema.proximo_estado(proximo_estado)



# HERANÇA de State parte principal do jogo

class Jogando(State):

    def __init__(self, sistema,
                 fundo=None,
                 musica='versao_final/src/musicas/jogo.mp3'):

        super().__init__(sistema, fundo, musica)
        self.sistema.tocar_musica(loop=True)

    
    # Executa toda a parte da logica do jogo até perder ou fechar a janela

    def executar(self):
        self.sistema.jogo.atualizar(self.sistema.dt)

        # quando o jogador fica sem vida, é passado para o proximo estado

        if self.sistema.jogo.final:
            self.sistema.proximo_estado(Final(self.sistema))



# HERANÇA de State, mostra as maiores pontuaçoes dos players

class Ranking(State):

    def __init__(self, sistema,
                 fundo="versao_final/src/backgrounds/tela_ranking.png",
                 musica=None):

        super().__init__(sistema, fundo, musica)
        self.sistema.atualizar_ranking()
        self.font = pygame.font.Font(
            'versao_final/src/fonte/pressstart.ttf', 24)
        self.texto_ranks = [self.font.render(f"{i+1} - {self.sistema.ranking[i][0]}:"+"{:.1f}".format(
            self.sistema.ranking[i][1]), True, pygame.Color('white')) for i in range(len(self.sistema.ranking))]
        self.button_voltar = pygame.Rect(20, 500, 224, 74)

    
    # Executa a tela de ranking ao clicar no botao

    def executar(self):
        self.sistema.desenhar_fundo()
        mx, my = pygame.mouse.get_pos()
        na_tela = 0
        posicao_y = 170
        for text in self.texto_ranks:
            if na_tela == 5:
                break

            tela.screen.blit(text, (240, posicao_y))
            posicao_y += 40
            na_tela += 1

        if self.sistema.click and self.button_voltar.collidepoint((mx, my)):
            self.efeito_sonoro.play()
            self.sistema.proximo_estado(Menu(self.sistema))

# HERANÇA de State, tela de lose

class Final(State):

    def __init__(self, sistema,
                 fundo="versao_final/src/backgrounds/tela_final.png",
                 musica='versao_final/src/musicas/game_over.mp3'):

        super().__init__(sistema, fundo, musica)
        self.sistema.tocar_musica()

        self.font = pygame.font.Font(
            'versao_final/src/fonte/pressstart.ttf', 16)
        self.button_salvar = pygame.Rect(705, 510, 210, 74)
        self.input_box = pygame.Rect(500, 172, 274, 40)
        self.button_menu = pygame.Rect(20, 500, 224, 74)
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('gray')
        self.color = self.color_inactive
        self.active = False
        self.nome = ''
        self.erro_msg = ''

    # Executa a tela final do jogo após perder todas as vidas

    def executar(self):
        self.sistema.desenhar_fundo()
        mx, my = pygame.mouse.get_pos()

        if self.sistema.click:
            self.active = self.input_box.collidepoint((mx, my))

        if self.active:
            for event in self.sistema.eventos:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.nome = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome = self.nome[:-1]
                    else:
                        self.nome += event.unicode

        # botao de salvar o nick do jogador, reiniciar o jogo, e passa para o proximo estado

        if self.button_salvar.collidepoint((mx, my)):
            if self.sistema.click:
                # tratamento de excesões de nome vazio e nome > que 15 caracteres
                try:
                    if self.nome != '':
                        if len(self.nome) <= 15:
                            self.sistema.salvar(self.nome)
                            self.efeito_sonoro.play()

                            self.sistema.reiniciar_jogo()
                            self.sistema.proximo_estado(Menu(self.sistema))

                        else:
                            raise Maior15_Caracteres
                    else:
                        raise NomeVazio
                except NomeVazio as e:
                    self.erro_msg = str(e)
                except Maior15_Caracteres as e:
                    self.erro_msg = str(e)

        # som ao clicar no botao

        if self.sistema.click and self.button_menu.collidepoint((mx, my)):
            self.efeito_sonoro.play()

            self.sistema.reiniciar_jogo()
            self.sistema.proximo_estado(Menu(self.sistema))

        # muda a cor

        self.color = self.color_active if self.active else self.color_inactive

        # renderiza texto

        txt_pontuacao = self.font.render("{:.1f}".format(
            self.sistema.jogo.pontuacao), True, pygame.Color("white"))
        txt_nome = self.font.render(self.nome, True, pygame.Color("white"))

        # desenha nome digitado

        tela.screen.blit(txt_nome, (self.input_box.x+5, self.input_box.y+10))

        # desenha pontuacao

        tela.screen.blit(txt_pontuacao, (400, 238))

        # caixa de input

        pygame.draw.rect(tela.screen, self.color, self.input_box, 2)

        # texto de erro e desenho
        
        txt_exception = self.font.render(
            self.erro_msg, True, pygame.Color("red"))
        tela.screen.blit(txt_exception, (190, 300))
