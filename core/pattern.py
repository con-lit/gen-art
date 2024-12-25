import cairosvg

from core.commons.enums import TileType


class Pattern:
    def __init__(self):
        files = [
            "arcs_1",
            "arcs_2",
            "arcs_4",
            "lines_1",
            "lines_2",
            "lines_4",
        ]
        self._files = {}
        for file in files:
            with open(f"static/svg/{file}.svg", "r") as f:
                svg_data = f.read()
                self._files[file] = svg_data

    def get(self, size:int, pattern:TileType) -> str:
        if size not in [1, 2, 4]:
            raise ValueError("Size must be one of 1, 2, 4")
        match pattern:
            case TileType.ARKS:
                key = f"arcs_{size}"
            case TileType.LINES:
                key = f"lines_{size}"
            case _:
                raise ValueError("Wrong tile type")
        svg_data = self._files[key]
        return svg_data
    
    def get_filename(self, size:int, pattern:str):
        if size not in [1, 2, 4]:
            raise ValueError("Size must be one of 1, 2, 4")
        if pattern not in ["round", "straight"]:    
            raise ValueError("Pattern must be one of 'round', 'straight'")
        return f"static/svg/{pattern}_{size}.svg"

