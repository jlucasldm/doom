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

class DoomEngine:
    def __init__(self, wad_path='wad/DOOM.WAD'):
        self.wad_path = wad_path
        self.on_init()

    def on_init(self):
        self.wad_data = WADData(self)

if __name__ == '__main__':
    doom = DoomEngine()