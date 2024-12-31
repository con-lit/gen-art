from flask import Flask, send_file, request, render_template
from io import BytesIO
from PIL import Image
import svgwrite
import cairo
from cairo import ImageSurface, FORMAT_ARGB32, Context
from core.color_theme import ColorTheme
from core.commons.constants import SHAPE, TILE_SIZE
from core.commons.enums import Design, Direction, Theme
from core.connector import Connector
from core.draw import draw
from core.fills.perlin import Perlin
from core.quadtree import QuadTree
import sys
sys.setrecursionlimit(10000)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bitmap')
def generate_bitmap():
    width = int(request.args.get('width', 100))
    height = int(request.args.get('height', 100))

    try:
        design = Design(str(request.args.get('design')))
    except ValueError:
        design = Design.MIXED

    try:
        directions = Direction(str(request.args.get('direction')))
    except ValueError:
        directions = Direction.MIXED
    
    try:
        theme = Theme(str(str(request.args.get('theme'))))
    except ValueError:
        theme = Theme.RANDOM
    
    cairo_surface= create_pattern(width, height, design, directions, theme)
    img = cairo_to_pil(cairo_surface)
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

def cairo_to_pil(surface: ImageSurface) -> Image:
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

def create_pattern(width:int, hight:int, design:Design, direction:Direction, theme:Theme) -> ImageSurface:
    k_width = divide_surface(width, TILE_SIZE, SHAPE)
    k_hight = divide_surface(hight, TILE_SIZE, SHAPE)

    quadtree = QuadTree((0, 0, k_width, k_hight),
                        matrix = Perlin(k_width, k_hight, octaves=3),
                        connector = Connector(k_width,
                                              k_hight,
                                              design = design,
                                              direction = direction))
    quadtree.connect()
    # quadtree.colorize(ColorTheme(theme))

    surface = ImageSurface(FORMAT_ARGB32, k_width*TILE_SIZE, k_hight*TILE_SIZE)
    ctx = Context(surface)
    quadtree.show(ctx, draw)
    return surface

if __name__ == '__main__':
    app.run(debug=True)