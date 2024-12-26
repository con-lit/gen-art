from core.commons.constants import SHAPE
from core.connector import Connector
from core.fills.perlin import Perlin
from math import floor

from core.tile import Tile


class QuadTree:
    def __init__(self, boundary:tuple, matrix:Perlin, connector: Connector, depth=0):
        self.boundary = boundary
        self.matrix = matrix
        self.depth = depth
        self.connector = connector
        if self.can_be_divided:
            if self.boundary[2] > SHAPE and self.boundary[3] > SHAPE:
                self._divide_surface()
            else:
                self._divide_quads()
        else:
            self.children = []
            self.tile = Tile(x=boundary[0],
                             y=boundary[1],
                             size=boundary[2],
                             connector=connector)

    @property
    def can_be_divided(self):
        return self.depth < 2 and self.matrix.max >0
    
    @property
    def divided(self):
        return bool(self.children)
    
    def _divide_surface(self):
        k_width = self.boundary[2]
        k_hight = self.boundary[3]
        self.children = []
        for y in range(0, k_hight, SHAPE):
            for x in range(0, k_width, SHAPE):
                boundary = (x, y, SHAPE, SHAPE)
                self.children.append(QuadTree(boundary,
                                              self.matrix.slice(x=boundary[0],
                                                                y=boundary[1],
                                                                size=boundary[2]),
                                              self.connector,
                                              self.depth + 1))

    def _divide_quads(self):
        x, y, s, s = self.boundary
        s_2 = floor(s / 2)
        nw = (x, y, s_2, s_2)
        ne = (x + s_2, y, s_2, s_2)
        sw = (x, y + s_2, s_2, s_2)
        se = (x + s_2, y + s_2, s_2, s_2)
        nw_slice = self.matrix.slice(0, 0, s_2)
        ne_slice = self.matrix.slice(s_2, 0, s_2)
        sw_slice = self.matrix.slice(0, s_2, s_2)
        se_slice = self.matrix.slice(s_2, s_2, s_2)
        self.children = [
            QuadTree(nw, nw_slice, self.connector, self.depth + 1),
            QuadTree(ne, ne_slice, self.connector, self.depth + 1),
            QuadTree(sw, sw_slice, self.connector, self.depth + 1),
            QuadTree(se, se_slice, self.connector, self.depth + 1),
        ]

    def show(self, ctx, draw):
        if self.divided:
            for child in self.children: child.show(ctx, draw)
        else:
            draw(ctx, self.tile)

    def colorize(self, color):
        if self.divided:
            for child in self.children: child.colorize(color)
        else:
            for stroke in  self.tile.strokes:
                stroke.set_color(color())
