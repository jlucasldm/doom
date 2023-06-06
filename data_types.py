# H - uint16,
# h - int16,
# I - uint32,
# i - int32,
# c - char,
# b - int8,
# B - uint8

class Thing:
    # 10 bytes
    __slots__ = [
        'pos', # pos_x, pos_y - 4h
        'angle',    # 2H
        'type',     # 2H
        'flags'     # 2H
    ]

class Seg:
    # 12 bytes = 2h * 6
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'angle',
        'linedef_id',
        'direction',
        'offset'
    ]

class Subsector:
    # 4 bytes = 2h + 2h
    __slots__ = ['seg_count', 'first_seg_id']

class Node:
    # 28 bytes = 2h * 12 + 2H * 2
    class Bbox:
        __slots__ = ['top', 'bottom', 'left', 'right']

    __slots__ = [
        'x_partition',
        'y_partition',
        'dx_partition',
        'dy_partition',
        'bbox',
        'front_child_id',
        'back_child_id'
    ]

    def __init__(self):
        self.bbox = {'front': self.Bbox(), 'back': self.Bbox()}

class Linedef:
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'flags',
        'line_type',
        'sector_tag',
        'front_sidedef_id',
        'back_sidedef_id'
    ]