from wad_reader import WADReader

# Classe que irá armazenar os dados do WAD
# A classe WADData irá instanciar a classe WADReader, passando o caminho do WAD
# A classe WADReader irá ler o arquivo WAD e armazenar os dados em uma lista de lumps
# A classe WADData irá fechar o arquivo WAD
class WADData:
    # Dicionário que irá armazenar os índices dos lumps do mapa
    # Ler https://doomwiki.org/wiki/Lump para mais informações
    LUMP_INDICES = {
        'THINGS': 1, 'LINEDEFS': 2, 'SIDEDEFS': 3,
        'VERTEXES': 4, 'SEGS': 5, 'SSECTORS': 6,
        'NODES': 7, 'SECTORS': 8, 'REJECT': 9,
        'BLOCKMAP': 10
    }
    def __init__(self, engine, map_name):
        self.reader = WADReader(engine.wad_path)    # Instanciar a classe WADReader, passando o caminho do WAD
        self.map_index = self.get_lump_index(lump_name=map_name) # Obter o índice do lump do mapa
        self.vertexes = self.get_lump_data(
            reader_func=self.reader.read_vertex,
            lump_index=self.map_index + self.LUMP_INDICES['VERTEXES'],
            num_bytes=4
        )
        self.linedefs = self.get_lump_data(
            reader_func=self.reader.read_linedef,
            lump_index=self.map_index + self.LUMP_INDICES['LINEDEFS'],
            num_bytes=14
        )
        self.nodes = self.get_lump_data(
            reader_func=self.reader.read_node,
            lump_index=self.map_index + self.LUMP_INDICES['NODES'],
            num_bytes=28
        )
        self.sub_sectors = self.get_lump_data(
            reader_func=self.reader.read_subsector,
            lump_index=self.map_index + self.LUMP_INDICES['SSECTORS'],
            num_bytes=4
        )
        self.segments = self.get_lump_data(
            reader_func=self.reader.read_segment,
            lump_index=self.map_index + self.LUMP_INDICES['SEGS'],
            num_bytes=12
        )
        self.things = self.get_lump_data(
            reader_func=self.reader.read_thing,
            lump_index=self.map_index + self.LUMP_INDICES['THINGS'],
            num_bytes=10
        )
        # [self.print_attrs(i) for i in self.linedefs]
        # print(f'\n{map_name}_index = {self.map_index}') # Imprimir o índice do lump do mapa
        # [print(i) for i in self.vertexes] # Imprimir os vértices do mapa
        self.reader.close() # Fechar o arquivo WAD

    @staticmethod
    def print_attrs(obj):
        print()
        for attr in obj.__slots__:
            print(eval(f'obj.{attr}'), end=' ')

    def get_lump_data(self, reader_func, lump_index, num_bytes, header_length=0):
        lump_info = self.reader.directory[lump_index] # Obter o dicionário com as informações do lump
        count = lump_info['lump_size'] // num_bytes # Obter o número de dados do lump
        data = []
        for i in range(count):
            offset = lump_info['lump_offset'] + i * num_bytes + header_length # Obter o offset do dado
            data.append(reader_func(offset)) # Obter o dado
        return data

    # Método que irá retornar o índice do lump referido por lump_name
    def get_lump_index(self, lump_name):
        # Para cada lump no diretório de lumps, temos um dicionário com as informações do lump
        # i é o índice do lump no diretório de lumps, lump_info é o dicionário com as informações do lump
        for i, lump_info in enumerate(self.reader.directory):
            if lump_name in lump_info.values():
                return i