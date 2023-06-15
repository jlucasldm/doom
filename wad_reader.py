# Struct reference: https://docs.python.org/3/library/struct.html
# WAD reference: https://doomwiki.org/wiki/WAD

# A biblioteca struct é utilizada para ler dados binários
import struct
from pygame.math import Vector2 as vec2
from data_types import *


# Cabe fazer algumas observações a respeito de um arquivo WAD. Um arquivo WAD é composto por 3 partes:
# 1. Header
# 2. Lump Data
# 3. Names and pointers to the lump data
# O header é composto por 12 bytes, sendo 4 bytes para o tipo de arquivo, 4 bytes para o número de lumps.
# Lumps são os dados do arquivo WAD, que podem ser mapas, texturas, sprites, etc.


class WADReader:
    def __init__(self, wad_path):
        self.wad_file = open(wad_path, 'rb')  # Abrir o arquivo WAD em modo binário
        self.header = self.read_header()  # Ler o header do arquivo WAD
        self.directory = self.read_directory()  # Ler o diretório de lumps do arquivo WAD
        print('\n', self.header)  # Imprimir o header do arquivo WAD
        [print('\n', lump) for lump in self.directory]  # Imprimir o diretório de lumps do arquivo WAD

    def read_thing(self, offset):
        # 10 bytes = 2h * 2 + 2H * 3
        read_2_bytes = self.read_2_bytes

        thing = Thing()
        x = read_2_bytes(offset=offset, byte_format='h')
        y = read_2_bytes(offset=offset + 2, byte_format='h')
        thing.angle = read_2_bytes(offset=offset + 4, byte_format='h')
        thing.type = read_2_bytes(offset=offset + 6, byte_format='h')
        thing.flags = read_2_bytes(offset=offset + 8, byte_format='h')
        thing.pos = vec2(x, y)

        return thing

    def read_segment(self, offset):
        # 12 bytes = 2h * 6
        read_2_bytes = self.read_2_bytes

        seg = Seg()
        seg.start_vertex_id = read_2_bytes(offset=offset, byte_format='h')
        seg.end_vertex_id = read_2_bytes(offset=offset + 2, byte_format='h')
        seg.angle = read_2_bytes(offset=offset + 4, byte_format='h')
        seg.linedef_id = read_2_bytes(offset=offset + 6, byte_format='h')
        seg.direction = read_2_bytes(offset=offset + 8, byte_format='h')
        seg.offset = read_2_bytes(offset=offset + 10, byte_format='h')

        return seg

    def read_subsector(self, offset):
        # 4 bytes = 2h * 2
        read_2_bytes = self.read_2_bytes

        subsector = Subsector()
        subsector.seg_count = read_2_bytes(offset=offset, byte_format='h')
        subsector.first_seg_id = read_2_bytes(offset=offset + 2, byte_format='h')

        return subsector

    def read_node(self, offset):
        # 28 bytes = 2h * 12 + 2h * 2
        read_2_bytes = self.read_2_bytes

        node = Node()
        node.x_partition = read_2_bytes(offset=offset, byte_format='h')
        node.y_partition = read_2_bytes(offset=offset + 2, byte_format='h')
        node.dx_partition = read_2_bytes(offset=offset + 4, byte_format='h')
        node.dy_partition = read_2_bytes(offset=offset + 6, byte_format='h')

        node.bbox['front'].top = read_2_bytes(offset=offset + 8, byte_format='h')
        node.bbox['front'].bottom = read_2_bytes(offset=offset + 10, byte_format='h')
        node.bbox['front'].left = read_2_bytes(offset=offset + 12, byte_format='h')
        node.bbox['front'].right = read_2_bytes(offset=offset + 14, byte_format='h')

        node.bbox['back'].top = read_2_bytes(offset=offset + 16, byte_format='h')
        node.bbox['back'].bottom = read_2_bytes(offset=offset + 18, byte_format='h')
        node.bbox['back'].left = read_2_bytes(offset=offset + 20, byte_format='h')
        node.bbox['back'].right = read_2_bytes(offset=offset + 22, byte_format='h')

        node.front_child_id = read_2_bytes(offset=offset + 24, byte_format='H')
        node.back_child_id = read_2_bytes(offset=offset + 26, byte_format='H')

        return node

    def read_linedef(self, offset):
        read_2_bytes = self.read_2_bytes

        linedef = Linedef()
        linedef.start_vertex_id = read_2_bytes(offset=offset, byte_format='h')
        linedef.end_vertex_id = read_2_bytes(offset=offset + 2, byte_format='h')
        linedef.flags = read_2_bytes(offset=offset + 4, byte_format='h')
        linedef.line_type = read_2_bytes(offset=offset + 6, byte_format='h')
        linedef.sector_tag = read_2_bytes(offset=offset + 8, byte_format='h')
        linedef.front_sidedef_id = read_2_bytes(offset=offset + 10, byte_format='h')
        linedef.back_sidedef_id = read_2_bytes(offset=offset + 12, byte_format='h')
        return linedef

    def read_vertex(self, offset):
        # 4 bytes = 2h + 2h
        x = self.read_2_bytes(offset=offset, byte_format='h')
        y = self.read_2_bytes(offset=offset + 2, byte_format='h')
        return vec2(x, y)

    # Ler o diretório de lumps do arquivo WAD
    def read_directory(self):
        directory = []
        for i in range(self.header['lump_count']):  # Para cada lump no diretório de lumps
            offset = self.header['info_table_offset'] + i * 16
            # Cada lump é definido por 16 bytes, sendo 4 bytes para o offset do lump,
            # 4 bytes para o tamanho do lump e 8 bytes para o nome do lump
            lump_info = {
                'lump_offset': self.read_4_bytes(offset=offset),
                'lump_size': self.read_4_bytes(offset=offset + 4),
                'lump_name': self.read_string(offset=offset + 8, num_bytes=8)
            }
            directory.append(lump_info)
        return directory

    # Ler o header do arquivo WAD. O header é composto por 12 bytes,
    # sendo 4 bytes para o tipo de arquivo, 4 bytes para o número de lumps e
    # 4 bytes para o offset da info table.
    def read_header(self):
        return {
            'wad_type': self.read_string(offset=0, num_bytes=4),  # Tipo de arquivo WAD
            'lump_count': self.read_4_bytes(offset=4),  # Número de lumps
            'info_table_offset': self.read_4_bytes(offset=8)  # Inteiro de 4 bytes que representa o ponteiro para
            # a localização do diretório de lumps
        }

    def read_1_byte(self, offset, byte_format):
        # b - int8, B - uint8
        return self.read_bytes(offset=offset, num_bytes=1, byte_format=byte_format)[0]

    def read_2_bytes(self, offset, byte_format):
        # h - int16, H - uint16
        return self.read_bytes(offset=offset, num_bytes=2, byte_format=byte_format)[0]

    # Método que irá ler um int32 dado um offset
    def read_4_bytes(self, offset, byte_format='i'):
        # i - int32, I - uint32
        return self.read_bytes(offset=offset, num_bytes=4, byte_format=byte_format)[0]

    # Método que irá ler uma string dado um offset e um número de bytes a serem lidos
    def read_string(self, offset, num_bytes):
        # c - char
        return ''.join(b.decode('ascii') for b in
                       self.read_bytes(offset=offset, num_bytes=num_bytes, byte_format='c' * num_bytes)
                       if ord(b) != 0).upper()

    # Método que irá ler os dados binários do arquivo WAD dado um offset, um número de bytes
    # a ser lido e um formato de bytes
    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)  # Ir para o offset especificado, em função da primeira posição do arquivo
        buffer = self.wad_file.read(num_bytes)  # Ler o número de bytes especificado
        return struct.unpack(byte_format, buffer)  # Desempacotar os bytes lidos de acordo com o formato especificado

    # Método para fecha o arquivo WAD
    def close(self):
        self.wad_file.close()
