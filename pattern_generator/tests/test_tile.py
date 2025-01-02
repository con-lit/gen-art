from core.connector import Connector
from core.quadtree import QuadTree
from core.tile import Tile


def test_tile():
    connector = Connector(4, 4)
    tile = Tile(0,0,4,connector)
    tile.connect()
    print(connector.horizontal_connections)