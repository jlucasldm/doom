# DOOM CLONE
#
# Após desenvolver um trabalho de computação gráfica, onde foi implementado um
# sistema de simulação de câmeras sobre uma maquete 3D, usando diversas formas de
# interação com o usuário, peguei gosto pela coisa. Criei o projeto em torno de
# um modelo da creepypasta Backrooms. Me empolguei com a manipulação de iluminação,
# movimentação da câmera e a possibilidade de criar um jogo de terror. Então, decidi
# dar um passo à frente no desenvolvimento de jogos e criar um clone do DOOM.
#
# Nunca joguei DOOM, mas já vi vídeos e sei que é um jogo de tiro em primeira pessoa
# com gráficos 3D. Gosto da ambientação e da trilha sonora. Acho que vai ser um bom
# desafio para aprender mais sobre desenvolvimento de jogos. Dar tiros em demônios ao
# som de heavy metal é do caralho demais, tá maluco filho.
#
# Vou usar como referência a série de vídeos tutoriais do canal Coder Space, disponível	
# em https://www.youtube.com/watch?v=KdYTvqZmyBk&list=PLi77irUVkDasNAYQPr3N8nVcJLQAlANva&pp=iAQB.
# O projeto será desenvolvido em Python, usando a biblioteca PyGame.
#
# O primeiro passo é ler o arquivo WAD, que contém os dados do jogo. O arquivo WAD
# é um arquivo de dados usado pela engine do DOOM para armazenar dados de níveis,
# gráficos, sons, música e outros. O arquivo WAD é dividido em lumps, que são
# estruturas de dados que armazenam informações sobre os dados do jogo. O arquivo
# WAD começa com um cabeçalho, que contém informações sobre o arquivo, como o tipo
# de arquivo, o número de lumps e o offset da tabela de informações. A tabela de
# informações contém informações sobre cada lump, como o nome, o tamanho e o offset
# do lump. O lump contém os dados do jogo, como os dados de um nível, um sprite ou
# um som.
#
# O arquivo WAD é um arquivo binário, então é necessário ler os dados em bytes.
# Para isso, é necessário usar a biblioteca struct, que permite ler e escrever
# dados binários. O primeiro passo é ler o cabeçalho do arquivo WAD. O cabeçalho
# contém 12 bytes, sendo 4 bytes para o tipo de arquivo, 4 bytes para o número de
# lumps e 4 bytes para o offset da tabela de informações. O tipo de arquivo é uma
# string de 4 caracteres, que pode ser IWAD ou PWAD. IWAD é o arquivo WAD principal
# do jogo, que contém os dados do jogo. PWAD é um arquivo WAD que contém dados
# adicionais, como um novo nível ou um novo sprite. O número de lumps é um inteiro
# de 4 bytes que indica o número de lumps no arquivo WAD. O offset da tabela de
# informações é um inteiro de 4 bytes que indica o offset da tabela de informações
# no arquivo WAD.
#
# Referências para informações a respeito do arquivo WAD pode ser encontrada em
# https://doomwiki.org/wiki/WAD e https://doomwiki.org/wiki/WAD_file_format.
from wad_data import WADData
from settings import *
from map_renderer import MapRenderer
import pygame as pg
import sys

class DoomEngine:
    # O construtor da classe DoomEngine recebe o caminho do arquivo WAD como parâmetro.
    def __init__(self, wad_path='wad/DOOM.WAD'):
        self.wad_path = wad_path    # O caminho do arquivo WAD é armazenado em uma variável.
        self.screen = pg.display.set_mode(WIN_RES)  # A tela do jogo é criada.
        self.clock = pg.time.Clock()    # O objeto Clock é criado para controlar o FPS.
        self.running = True # A variável running é usada para controlar o loop principal do jogo.
        self.dt = 1/60   # A variável dt é usada para controlar o FPS.
        self.on_init()  # O método on_init é chamado no construtor da classe DoomEngine.

    # O método on_init cria uma instância da classe WADData, que é responsável por
    # ler os dados do arquivo WAD.
    def on_init(self):
        self.wad_data = WADData(self, map_name='E1M1') # Instanciar a classe WADData, passando o caminho do arquivo WAD e o nome do mapa.
        self.map_renderer = MapRenderer(self)  # Instanciar a classe MapRenderer, passando a instância da classe DoomEngine.

    def update(self):
        # O método update é chamado a cada frame do jogo.
        self.dt = self.clock.tick()
        pg.display.flip()   # Atualizar a tela do jogo.
        pg.display.set_caption(f'Doom Clone - FPS: {self.clock.get_fps():.2f}') # Atualizar o título da janela do jogo.

    def draw(self):
        self.screen.fill('black') # Preencher a tela do jogo com a cor preta.
        self.map_renderer.draw()  # O método draw da classe MapRenderer é chamado a cada frame do jogo.

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.check_events() # O método check_events é chamado a cada frame do jogo.
            self.update()   # O método update é chamado a cada frame do jogo.
            self.draw() # O método draw é chamado a cada frame do jogo.
        pg.quit()   # Encerrar o PyGame.
        sys.exit()  # Encerrar o programa.

# __name__ é uma variável especial do Python que armazena o nome do módulo.
# Se o módulo for executado diretamente, o valor de __name__ é __main__.
# Se o módulo for importado, o valor de __name__ é o nome do módulo.
if __name__ == '__main__':
    # Se o módulo for executado diretamente, cria uma instância da classe DoomEngine.
    doom = DoomEngine()
    doom.run()  # Chama o método run da classe DoomEngine.