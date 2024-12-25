from dataclasses import dataclass
from core.commons.enums import Side
from core.tile import Tile

@dataclass
class Link:
    tile: Tile
    side: Side
    interface_id: int

@dataclass
class Connector:
    link:Link
    stroke_id:int
