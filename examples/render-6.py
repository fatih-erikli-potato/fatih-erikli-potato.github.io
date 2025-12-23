from render import render
from ball import create_ball
from bezier import bezier, lerp
from xyz_on_canvas import xyz_on_canvas

from PIL import Image, ImageDraw

def distance(a, b):
  ax, ay, az = a
  bx, by, bz = b
  dx = max(ax, bx) - min(ax, bx)
  dy = max(ay, by) - min(ay, by)
  dz = max(az, bz) - min(az, bz)
  return max(dx, dy, dz)

WIDTH = 1024
HEIGHT = 1024
UNIT_SCALE = 2
ROTATE_H = 40
ROTATE_V = 20

surface = [
  [[-40,0,-40],[4,0,-40],[40,0,-4],[40,0,40]],
  [[-40,0,-16],[-6,0,-16],[16,0,6],[16,0,40]],
  [[-40,-16,0],[-16,-16,0],[0,-16,16],[0,-16,40]],
  [[-40,-40,0],[-16,-40,0],[0,-40,16],[0,-40,40]]
]

scale_surface = 4

for curve in surface:
  for p in curve:
    p[0] *= scale_surface
    p[1] *= scale_surface
    p[2] *= scale_surface

wide = 10
fall = 10
ball_size = 2
faces = []

for w in range(0, wide):
  wa = bezier(w/wide, surface[0][0], surface[0][1], surface[0][2], surface[0][3])
  wb = bezier(w/wide, surface[1][0], surface[1][1], surface[1][2], surface[1][3])
  wc = bezier(w/wide, surface[2][0], surface[2][1], surface[2][2], surface[2][3])
  wd = bezier(w/wide, surface[3][0], surface[3][1], surface[3][2], surface[3][3])
  wa_next = bezier((w+1)/wide, surface[0][0], surface[0][1], surface[0][2], surface[0][3])
  wb_next = bezier((w+1)/wide, surface[1][0], surface[1][1], surface[1][2], surface[1][3])
  wc_next = bezier((w+1)/wide, surface[2][0], surface[2][1], surface[2][2], surface[2][3])
  wd_next = bezier((w+1)/wide, surface[3][0], surface[3][1], surface[3][2], surface[3][3])
  for f in range(0, fall):
    a = bezier(f/fall, wa, wb, wc, wd)
    b = bezier(f/fall, wa_next, wb_next, wc_next, wd_next)
    c = bezier((f+1)/fall, wa_next, wb_next, wc_next, wd_next)
    d = bezier((f+1)/fall, wa, wb, wc, wd)
    faces.append([a, b, c, d, 255, 255, 255])

def zsort(cube):
  x, y, z, r, g, b = cube
  return (y, z, x)

faces_rendered = []

for a, b, c, d, *rgb in faces:
  cubes = []
  segments_wide = max(distance(a,b), distance(d, c))
  for i in range(0, int(segments_wide)):
    linea = lerp(i/segments_wide, a, b)
    lineb = lerp(i/segments_wide, d, c)
    segments_line = distance(linea, lineb)
    for j in range(0, int(segments_line)):
      px, py, pz = lerp(j/segments_line, linea, lineb)
      for x, y, z in create_ball(ball_size):
        cubes.append([px + x, py + y, pz + z, *rgb])
  cubes.sort(key=zsort)
  img = render(
    "face",
    cubes,
    WIDTH,
    HEIGHT,
    UNIT_SCALE,
    ROTATE_H,
    ROTATE_V,
    False
  )
  widthimg, heightimg = img.size
  pixels = img.load()
  shade_len = 0
  sum_r = 0
  sum_g = 0
  sum_b = 0
  for x in range(widthimg):
    for y in range(heightimg):
      rgb = pixels[x, y]
      if not (rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255):
        # white is the background color
        sum_r += rgb[0]
        sum_g += rgb[1]
        sum_b += rgb[2]
        shade_len += 1
  avg_r = sum_r / shade_len
  avg_g = sum_g / shade_len
  avg_b = sum_b / shade_len
  faces_rendered.append([a, b, c, d, [int(avg_r), int(avg_g), int(avg_b)]])

name = "render-6-1"
width = WIDTH * UNIT_SCALE
height = HEIGHT * UNIT_SCALE
image = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(image)
faces_on_canvas = []

for a, b, c, d, rgb in faces_rendered:
  points = []
  for x, y, z in [a, b, c, d]:
    points.append(xyz_on_canvas(x, y, z, UNIT_SCALE, width, height, ROTATE_H, ROTATE_V, True))
  faces_on_canvas.append([points, rgb])

def centerz_sort(face):
  points, rgb = face
  sumz = 0
  for x, y, z in points:
    z += sumz
  return sumz / len(points)
faces_on_canvas.sort(key=centerz_sort)
for face in faces_on_canvas:
  points, rgb = face
  points_wo_z = []
  for x, y, z in points:
    points_wo_z.append((x, y))
  draw.polygon(points_wo_z, tuple(rgb))

image.save(open("{}.png".format(name), "wb"), "PNG")