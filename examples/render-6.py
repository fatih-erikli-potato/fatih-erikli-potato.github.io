from create_cube import create_cube
from darken import darken
from carboncopy import carboncopy
from ball import create_ball
from bezier import bezier, lerp
from rotate import rotate_xyz
import math

from PIL import Image, ImageDraw

def centerz_sort(face):
  points, rgb = face
  sumz = 0
  for x, y, z in points:
    z += sumz
  return sumz / len(points)

def render(name, cubes, width, height, unit_scale, rotate_horizontal, rotate_vertical):
  width *= unit_scale
  height *= unit_scale
  image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
  draw = ImageDraw.Draw(image)
  faces = []
  for x, y, z, r, g, b in cubes:
    cube = create_cube(x, y, z, rotate_horizontal, rotate_vertical)
    for darken_percent, *diamond in cube:
      points = []
      for xx, yy, zz in diamond:
        xn, yn, zn = rotate_xyz(
          xx * unit_scale,
          yy * unit_scale,
          zz * unit_scale,
          rotate_horizontal,
          rotate_vertical
        )
        points.append([xn, yn, zn])
      faces.append([points, darken(r, g, b, darken_percent)])
  faces.sort(key=centerz_sort)
  for abcd, rgb in faces:
    points = []
    for xx, yy, zz in abcd:
      x = width/2 + xx
      y = height/2 + (yy * -1)
      points.append((x, y))
    draw.polygon(points, (*rgb, 255))
  return image

def distance(a, b):
  ax, ay, az = a
  bx, by, bz = b
  dx = max(ax, bx) - min(ax, bx)
  dy = max(ay, by) - min(ay, by)
  dz = max(az, bz) - min(az, bz)
  return max(dx, dy, dz)

WIDTH = 512
HEIGHT = 512
UNIT_SCALE = 10
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

wide = 4
fall = 4
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

def avg_rgb(carbon_copy, img):
  widthimg, heightimg = img.size
  pixels = img.load()
  shade_len = 0
  sum_r = 0
  sum_g = 0
  sum_b = 0
  for x in range(widthimg):
    for y in range(heightimg):
      rgb = pixels[x, y]
      ccrgb = carbon_copy.getpixel((x, y))
      if ccrgb[0] == 0 and ccrgb[1] == 0 and ccrgb[2] == 0:
        sum_r += rgb[0]
        sum_g += rgb[1]
        sum_b += rgb[2]
        shade_len += 1
  if shade_len == 0:
    return (255, 255, 255)
  avg_r = int(sum_r / shade_len)
  avg_g = int(sum_g / shade_len)
  avg_b = int(sum_b / shade_len)
  return (avg_r, avg_g, avg_b)

faces_rendered = []

face_index = 0
for a, b, c, d, *rgb in faces:
  cubes = []
  segments_wide = max(distance(a,b), distance(d, c))
  for i in range(0, math.ceil(segments_wide)):
    linea = lerp(i/segments_wide, a, b)
    lineb = lerp(i/segments_wide, d, c)
    segments_line = distance(linea, lineb)
    for j in range(0, math.ceil(segments_line)):
      px, py, pz = lerp(j/segments_line, linea, lineb)
      cubes.append([px, py, pz, *rgb])
  img = render(
    "face",
    cubes,
    WIDTH,
    HEIGHT,
    UNIT_SCALE,
    ROTATE_H,
    ROTATE_V
  )  
  carbon_copy = carboncopy([a, b, c, d], WIDTH, HEIGHT, UNIT_SCALE, ROTATE_H, ROTATE_V)
  carbon_copy_over = carboncopy([a, b, c, d], WIDTH, HEIGHT, UNIT_SCALE, ROTATE_H, ROTATE_V, (0, 0, 255, 100))
  imgcarboncopyover = img.copy()
  imgcarboncopyover.alpha_composite(carbon_copy_over)
  rr, gg, bb = avg_rgb(carbon_copy, img)
  faces_rendered.append([a, b, c, d, rr, gg, bb])
  renderedface = carboncopy([a, b, c, d], WIDTH, HEIGHT, UNIT_SCALE, ROTATE_H, ROTATE_V, (rr, gg, bb, 255))
  img.save(open("painting/cubes-{0}.png".format(face_index), "wb"), "PNG")
  imgcarboncopyover.save(open("painting/carboncopy-over-{0}.png".format(face_index), "wb"), "PNG")
  carbon_copy.save(open("painting/carboncopy-{0}.png".format(face_index), "wb"), "PNG")
  renderedface.save(open("painting/rendered-{0}.png".format(face_index), "wb"), "PNG")
  face_index += 1

def draw_rendered_faces(name, faces_rendered, rh, rv):
  width = WIDTH * UNIT_SCALE
  height = HEIGHT * UNIT_SCALE
  image = Image.new("RGB", (width, height), (255, 255, 255))
  draw = ImageDraw.Draw(image)
  faces_on_canvas = []

  for a, b, c, d, *rgb in faces_rendered:
    points = []
    for x, y, z in [a, b, c, d]:
      # it is possible to see the render in different angles than painting
      xn, yn, zn = rotate_xyz(x * UNIT_SCALE, y * UNIT_SCALE, z * UNIT_SCALE, rh, rv)
      points.append((xn, yn, zn))
    faces_on_canvas.append([points, rgb])

  faces_on_canvas.sort(key=centerz_sort)

  for face in faces_on_canvas:
    points, rgb = face
    points_wo_z = []
    for x, y, z in points:
      points_wo_z.append(( width/2 + x, height/2 + y*-1))
    draw.polygon(points_wo_z, tuple(rgb))

  image.save(open("{}.png".format(name), "wb"), "PNG")

# draw_rendered_faces("render-6", faces_rendered, ROTATE_H, ROTATE_V)
# draw_rendered_faces("render-6-1", faces_rendered, ROTATE_H, ROTATE_V)
# draw_rendered_faces("render-6-2", faces_rendered, ROTATE_H + 10, ROTATE_V)
# draw_rendered_faces("render-6-3", faces_rendered, ROTATE_H + 20, ROTATE_V)