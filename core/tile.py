import uuid
from core.commons.constants import STROKES_PER_CELL
import random
import math
from typing import List, Dict

from core.commons.enums import Side, TileType
from core.connector import Connector
from core.stroke import Stroke

class Tile:
    def __init__(self, x: int, y: int, size: int, connector: Connector):
        self.strokes = [Stroke() for _ in range(size * STROKES_PER_CELL * 2 + 1)]
        self.uuid = uuid.uuid4()
        self._x = x
        self._y = y
        self._size = size
        self._connector = connector
        self._type = TileType.ARKS #random.choice(list(TileType))
        self._rotation_index = random.randint(0, 3)
        self._interfaces = {}
        self._register_links()
        self._side_indexes = self._create_indexes()
        self._connect()

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def size(self):
        return self._size
    
    @property
    def type(self):
        return self._type

    @property
    def rotation(self):
        return self._rotation_index * math.pi / 2

    def _register_links(self):
        for i in range(self._size):
            self._connector.register_connections(self, i)

    def _reverse_interfaces(self, input: List[List[int]]) -> List[List[int]]:
        return [list(reversed(lst)) for lst in reversed(input)]

    def _create_indexes(self) -> Dict[Side, List[List[int]]]:
        top, bottom, left, right = [], [], [], []
        output = {}

        match self._type:
            case TileType.ARKS:
                '''
                top = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
                '''
                top = [
                    [interface_id * STROKES_PER_CELL + id for id in range(STROKES_PER_CELL + 1)]
                        for interface_id in range(self._size)
                ]
                bottom = [
                    [self._size * STROKES_PER_CELL + interface_id * STROKES_PER_CELL + id for id in range(STROKES_PER_CELL + 1)]
                        for interface_id in range(self._size)
                ]
                left = [list(e) for e in top]
                right = [list(e) for e in bottom]
            case TileType.LINES:
                top = [[interface_id * STROKES_PER_CELL + color_id for color_id in range(STROKES_PER_CELL + 1)] for interface_id in range(self._size)]
                left = [[self._size * STROKES_PER_CELL + interface_id * STROKES_PER_CELL + color_id for color_id in range(STROKES_PER_CELL + 1)] for interface_id in range(self._size)]
                right = [list(e) for e in left]
                bottom = [list(e) for e in top]

                top_left = top[0][0]
                bottom_right = top[-1][-1]

                left[0][0] = top_left
                left[-1][-1] = top_left
                right[-1][-1] = bottom_right
            case _:
                raise ValueError(f"Invalid tile type {self._type}")

        match self._rotation_index:
            case 0:
                output = {
                    Side.TOP: top,
                    Side.RIGHT: right,
                    Side.BOTTOM: bottom,
                    Side.LEFT: left,
                }
            case 1:
                output = {
                    Side.TOP: self._reverse_interfaces(left),
                    Side.RIGHT: top,
                    Side.BOTTOM: self._reverse_interfaces(right),
                    Side.LEFT: bottom,
                }
            case 2:
                output = {
                    Side.TOP: self._reverse_interfaces(bottom),
                    Side.RIGHT: self._reverse_interfaces(left),
                    Side.BOTTOM: self._reverse_interfaces(top),
                    Side.LEFT: self._reverse_interfaces(right),
                }
            case 3:
                output = {
                    Side.TOP: right,
                    Side.RIGHT: self._reverse_interfaces(bottom),
                    Side.BOTTOM: left,
                    Side.LEFT: self._reverse_interfaces(top),
                }
            case _: 
                raise ValueError(f"Invalid rotation index {self._rotation_index}")

        return output

    def _connect(self):
        self._interfaces = {side: [] for side in Side}
        for side in self._interfaces.keys():
            interface_side = [self._connector.get_connection(self._x,
                                                             self._y,
                                                             self._size,
                                                             side, 
                                                             interface_id) for interface_id in range(self._size)]
            self._interfaces[side] = interface_side

        for input_side in self._interfaces.keys():
            side_interfaces = self._interfaces[input_side]
            for interface_id in range(len(side_interfaces)):
                for stroke_id in range(STROKES_PER_CELL + 1):
                    index = self._side_indexes[input_side][interface_id][stroke_id]
                    link = self._interfaces[input_side][interface_id]
                    self.strokes[index].add_link(input_side, link, stroke_id)

    def color_stroke(self, new_color, input_side, interface_id, stroke_id):
        index = self._side_indexes[input_side][interface_id][stroke_id]
        if index is not None:
            self.strokes[index].set_color(new_color)

    def color_stroke_with_id(self, index):
        self.strokes[index].set_color("amberAccent")
