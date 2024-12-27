from core.commons.enums import Side
from core.commons.data_classes import Link


class Connector:
  def __init__(self, width: int, height: int):
    if not (width > 0 and height > 0):
      raise ValueError("Width and height must be greater than 0.")
    self.horizontal_connections = [[[] for _ in range(width)] for _ in range(height + 1)]
    self.vertical_connections = [[[] for _ in range(width + 1)] for _ in range(height)]
  
  vertical_connections = []
  horizontal_connections = []
  registered_interfaces:int = 0

  def register_connections(self, tile, id: int):
    x = tile.x
    y = tile.y
    print("register:", x,y,id)

    self.vertical_connections[y + id][x].append(Link(tile, Side.LEFT, id))
    self.vertical_connections[y + id][x + tile.size].append(Link(tile, Side.RIGHT, id))
    self.horizontal_connections[y][x + id].append(Link(tile, Side.TOP, id))
    self.horizontal_connections[y + tile.size][x + id].append(Link(tile, Side.BOTTOM, id))
    self.registered_interfaces += 1

  def get_connection(self, tile, side: Side, id: int):
    connections = []

    match side:
      case Side.LEFT:
        connections = self.vertical_connections[tile.y + id][tile.x]
      case Side.RIGHT:
        connections = self.vertical_connections[tile.y + id][tile.x + tile.size]
      case Side.TOP:
        connections = self.horizontal_connections[tile.y][tile.x + id]
      case Side.BOTTOM:
        connections = self.horizontal_connections[tile.y + tile.size][tile.x + id]
    try:
      output_link = next(e for e in connections if e.tile != tile)
      return output_link
    except StopIteration:
      print(connections)
      print(f"Connection not found for {tile.x}, {tile.y}, {tile.size}, {side}, {tile.uuid}")
      return None