from core.commons.enums import Side

class Connector:
  def __init__(self, width: int, height: int):
    if not (width > 0 and height > 0):
      raise ValueError("Width and height must be greater than 0.")
    self.horizontal_connections = [[[] for _ in range(width)] for _ in range(height + 1)]
    self.vertical_connections = [[[] for _ in range(width + 1)] for _ in range(height)]
  
  vertical_connections = []
  horizontal_connections = []
  registered_interfaces:int = 0

  def register_connections(self, tile, interface_id: int):
    from core.commons.data_classes import Link
    x = tile.x
    y = tile.y

    self.vertical_connections[y + interface_id][x].append(Link(tile, Side.LEFT, interface_id))
    self.vertical_connections[y + interface_id][x + tile.size].append(Link(tile, Side.RIGHT, interface_id))
    self.horizontal_connections[y][x + interface_id].append(Link(tile, Side.TOP, interface_id))
    self.horizontal_connections[y + tile.size][x + interface_id].append(Link(tile, Side.BOTTOM, interface_id))
    self.registered_interfaces += 1

  def get_connection(self, x: int, y: int, size: int, side: Side, id: int):
    connections = []

    match side:
      case Side.LEFT:
        connections = self.vertical_connections[y + id][x]
      case Side.RIGHT:
        connections = self.vertical_connections[y + id][x + size]
      case Side.TOP:
        connections = self.horizontal_connections[y][x + id]
      case Side.BOTTOM:
        connections = self.horizontal_connections[y + size][x + id]

    try:
      output_link = next(e for e in connections if e.interface_id != id)
      return output_link
    except StopIteration:
      return None
