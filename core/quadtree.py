from core.connector import Connector
from core.perlin import Perlin
from math import floor

from core.tile import Tile


class QuadTree:
    def __init__(self, boundary:tuple, matrix:Perlin, connector: Connector, depth=0):
        self.boundary = boundary
        self.perlin = matrix
        self.depth = depth
        if self.can_be_divided:
            self._divide()
        else:
            self.children = []
            self.tile = Tile(*boundary)

    @property
    def can_be_divided(self):
        return self.depth < 2 and self.perlin.max >0
    
    @property
    def divided(self):
        return bool(self.children)

    def _divide(self):
        x, y, s = self.boundary
        s_2 = floor(s / 2)
        nw = (x, y, s_2)
        ne = (x + s_2, y, s_2)
        sw = (x, y + s_2, s_2)
        se = (x + s_2, y + s_2, s_2)
        nw_slice = self.perlin.slice(0, 0, s_2)
        ne_slice = self.perlin.slice(s_2, 0, s_2)
        sw_slice = self.perlin.slice(0, s_2, s_2)
        se_slice = self.perlin.slice(s_2, s_2, s_2)
        self.children = [
            QuadTree(nw, nw_slice, self.depth + 1),
            QuadTree(ne, ne_slice, self.depth + 1),
            QuadTree(sw, sw_slice, self.depth + 1),
            QuadTree(se, se_slice, self.depth + 1),
        ]

    def show(self, ctx, draw):
        if self.divided:
            for child in self.children: child.show(ctx, draw)
        else:
            draw(ctx, self.tile)

    def connect(self):
        if self.divided:
            for child in self.children: child.connect()
        else:
            self.tile.connect()

    def colorize(self, color):
        if self.divided:
            for child in self.children: child.colorize(color)
        else:
            for stroke in  self.tile.strokes:
                stroke.set_color(color())
