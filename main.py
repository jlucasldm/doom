from wad_data import WADData
from settings import *
from map_renderer import MapRenderer
from player import Player
from bsp import BSP
import pygame as pg
import sys


class DoomEngine:
    # O construtor da classe DoomEngine recebe o caminho do arquivo WAD como parâmetro.
    def __init__(self, wad_path='wad/DOOM.WAD'):
        self.wad_data = None
        self.map_renderer = None
        self.wad_path = wad_path        # O caminho do arquivo WAD é armazenado em uma variável.
        self.screen = pg.display.set_mode(WIN_RES)  # A tela do jogo é criada.
        self.clock = pg.time.Clock()    # O objeto Clock é criado para controlar o FPS.
        self.running = True             # A variável running é usada para controlar o loop principal do jogo.
        self.dt = 1/60                  # A variável dt é usada para controlar o FPS.
        self.on_init()                  # O método on_init é chamado no construtor da classe DoomEngine.

    # O método on_init cria uma instância da classe WADData, que é responsável por
    # ler os dados do arquivo WAD.
    def on_init(self):
        self.wad_data = WADData(self, map_name='E1M1')  # Instanciar a classe WADData, passando o caminho do arquivo
        # WAD e o nome do mapa.
        self.map_renderer = MapRenderer(self)           # Instanciar a classe MapRenderer, passando a instância da
        # classe DoomEngine.
        self.player = Player(self)                      # Instanciar a classe Player, passando a instância da classe
        # DoomEngine.
        self.bsp = BSP(self)                            # Instanciar a classe BSP, passando a instância da classe
        # DoomEngine.

    def update(self):
        self.player.update()  # O método update da classe Player é chamado a cada frame do jogo.
        self.bsp.update()     # O método update da classe BSP é chamado a cada frame do jogo.
        self.dt = self.clock.tick()
        pg.display.set_caption(f'Doom Clone - FPS: {self.clock.get_fps():.2f}')  # Atualizar o título da janela do jogo.

    def draw(self):
        self.screen.fill('black')   # Preencher a tela do jogo com a cor preta.
        self.map_renderer.draw()    # O método draw da classe MapRenderer é chamado a cada frame do jogo.
        pg.display.flip()  # Atualizar a tela do jogo.

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.check_events()     # O método check_events é chamado a cada frame do jogo.
            self.update()           # O método update é chamado a cada frame do jogo.
            self.draw()             # O método draw é chamado a cada frame do jogo.
        pg.quit()   # Encerrar o PyGame.
        sys.exit()  # Encerrar o programa.


# __name__ é uma variável especial do Python que armazena o nome do módulo.
# Se o módulo for executado diretamente, o valor de __name__ é __main__.
# Se o módulo for importado, o valor de __name__ é o nome do módulo.


if __name__ == '__main__':
    # Se o módulo for executado diretamente, cria uma instância da classe DoomEngine.
    doom = DoomEngine()
    doom.run()  # Chama o método run da classe DoomEngine.
