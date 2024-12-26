import random
from typing import List
import cairosvg
from flask import Flask, send_file, request, render_template
from io import BytesIO
from PIL import Image
import svgwrite
import cairo
from cairo import ImageSurface, FORMAT_ARGB32, Context
from core.commons.constants import SHAPE, TILE_SIZE
from core.connector import Connector
from core.pattern import Pattern
from core.fills.perlin import Perlin
from core.quadtree import QuadTree


app = Flask(__name__)

patterns = Pattern()

def monochrome_color() -> tuple:
    colors = [
        (0x2B, 0x45, 0x0E),
        (0xAB, 0xCE, 0x86),
        (0x79, 0xC4, 0x29),
        (0x45, 0x64, 0x23),
        (0x5A, 0x91, 0x1F),
    ]
    return random.choice(colors)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bitmap')
def generate_bitmap():
    width = int(request.args.get('width', 100))
    height = int(request.args.get('height', 100))
    cairo_surface= create_pattern(width, height)
    img = to_pil(cairo_surface)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/svg')
def generate_svg():
    dwg = svgwrite.Drawing(size=(100, 100))
    dwg.add(dwg.rect(insert=(0, 0), size=(100, 100), fill='blue'))
    buf = BytesIO()
    dwg.write(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/svg+xml')

def to_pil(surface: ImageSurface) -> Image:
    format = surface.get_format()
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        if format == cairo.Format.RGB24:
            return Image.frombuffer(
                "RGB", size, memory.tobytes(),
                'raw', "BGRX", stride)
        elif format == cairo.Format.ARGB32:
            return Image.frombuffer(
                "RGBA", size, memory.tobytes(),
                'raw', "BGRa", stride)
        else:
            raise NotImplementedError(repr(format))
        
def get_sublist(array, x1, x2, y1, y2):
    return [row[y1:y2+1] for row in array[x1:x2+1]]

def divide_surface(l, s, m):
    k = l // s + 1
    k = (k // m + 1) * m if k % m != 0 else k
    return k

def create_pattern(width:int, hight:int) -> ImageSurface:
    k_width = divide_surface(width, TILE_SIZE, SHAPE)
    k_hight = divide_surface(hight, TILE_SIZE, SHAPE)

    quadtree = QuadTree((0, 0, k_width, k_hight),
                        matrix = Perlin(k_width, k_hight, octaves=3),
                        connector = Connector(k_width, k_hight))
    quadtree.colorize(monochrome_color)

    surface = ImageSurface(FORMAT_ARGB32, k_width*TILE_SIZE, k_hight*TILE_SIZE)
    ctx = Context(surface)
    quadtree.show(ctx, draw)
    return surface

from core.tile import Tile
def draw(ctx, tile:Tile):
    x = tile.x
    y = tile.y
    s = tile.size
    screen_size = s * TILE_SIZE
    svg_data = patterns.get(s, tile.type)
    for i, stroke in enumerate(tile.strokes):
        hex_color = f'#{stroke.color[0]:02x}{stroke.color[1]:02x}{stroke.color[2]:02x}'
        svg_data = svg_data.replace(f'color{i}', hex_color)
    bytes = cairosvg.svg2png(bytestring=svg_data,
                             output_height=screen_size,
                             output_width=screen_size,)  
    surface = cairo.ImageSurface.create_from_png(BytesIO(bytes))
    ctx.save()
    ctx.translate(x * TILE_SIZE + (s * TILE_SIZE) / 2, y * TILE_SIZE + (s * TILE_SIZE) / 2)
    ctx.rotate(tile.rotation)
    ctx.translate(-(s * TILE_SIZE) / 2, -(s * TILE_SIZE) / 2)
    ctx.set_source_surface(surface, 0, 0)
    ctx.paint()
    ctx.restore()

def get_tiles_at(x, y) -> List[Tile]:
    pass
    

if __name__ == '__main__':
    app.run(debug=True)