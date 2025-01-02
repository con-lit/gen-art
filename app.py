from flask import Flask, send_file, request, render_template
from io import BytesIO
import svgwrite
from core.commons.enums import Design, Direction, Theme
import sys

from core.pattern_creater import truchet_tiles
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
    
    image = truchet_tiles(width, height, design, directions, theme)
    
    return send_file(image, mimetype='image/png')

@app.route('/svg')
def generate_svg():
    dwg = svgwrite.Drawing(size=(100, 100))
    dwg.add(dwg.rect(insert=(0, 0), size=(100, 100), fill='blue'))
    buf = BytesIO()
    dwg.write(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/svg+xml')
        
def get_sublist(array, x1, x2, y1, y2):
    return [row[y1:y2+1] for row in array[x1:x2+1]]

if __name__ == '__main__':
    app.run(debug=True)