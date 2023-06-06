# Código de teste e assimilação do conceito de Binary Space Partitioning (BSP)
# id Software, ao negociar a distribuição de Wolfenstein 3D com a Nintendo, precisou
# lidar com as limitações de memória do console, que impossibilitavam o uso de um
# algoritmo de raycasting a uma taxa de framerate aceitável. Para contornar esse problema,
# John Carmack descobriu o artigo "Constructing Good Partitioning Trees" de Bruce Naylor,
# cujo conteúdo foi utilizado para implementar o algoritmo de Binary Space Partitioning em
# Wolfeinstein 3D. O algoritmo de BSP consiste em dividir o mapa em partições, de forma que
# cada partição seja dividida em partições menores, até que cada partição contenha apenas
# um segmento de reta. A partir daí, o algoritmo de raycasting é aplicado em cada segmento
# de reta, de forma que o número de segmentos de reta a serem testados seja reduzido.

# O artigo está disponível em: https://graphicsinterface.org/wp-content/uploads/gi1993-27.pdf

# Esse código é uma tentativa de assimilar o conceito de BSP, utilizando o algoritmo de
# Binary Space Partitioning para dividir um mapa 1D em partições.
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def insert(node, value):
    if value < node.value:
        if node.left:
            insert(node.left, value)
        else:
            node.left = Node(value)
    elif value > node.value:
        if node.right:
            insert(node.right, value)
        else:
            node.right = Node(value)


def traverse(node, player_pos):
    if node:
        if player_pos <= node.value:
            traverse(node.left, player_pos)
            print(node.value, end=' ')
            traverse(node.right, player_pos)
        else:
            traverse(node.right, player_pos)
            print(node.value, end=' ')
            traverse(node.left, player_pos)


if __name__ == '__main__':
    root = Node(0)
    [insert(root, value) for value in [-15, -8, 6, 12, 20]]
    traverse(root, player_pos=9)
