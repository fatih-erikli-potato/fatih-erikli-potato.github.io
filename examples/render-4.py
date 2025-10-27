from render import render
from ball import create_ball
from bezier import bezier
import math

def makeid(x, y, z):
  return "{0}:{1}:{2}".format(x, y, z)

cubes = []
cubes_in_scene = set()

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

wide = 200
fall = 200

for w in range(0, wide):
  wa = bezier(w/wide, surface[0][0], surface[0][1], surface[0][2], surface[0][3])
  wb = bezier(w/wide, surface[1][0], surface[1][1], surface[1][2], surface[1][3])
  wc = bezier(w/wide, surface[2][0], surface[2][1], surface[2][2], surface[2][3])
  wd = bezier(w/wide, surface[3][0], surface[3][1], surface[3][2], surface[3][3])
  for f in range(0, fall):
    px, py, pz = bezier(f/fall, wa, wb, wc, wd)
    for x, y, z in create_ball(5):
      cubex = math.floor(px + x)
      cubey = math.floor(py + y)
      cubez = math.floor(pz + z)
      cubeid = makeid(cubex, cubey, cubez)
      if not cubeid in cubes_in_scene:
        cubes.append([cubex, cubey, cubez, 255, 255, 255])
        cubes_in_scene.add(cubeid)

def zsort(cube):
  x, y, z, r, g, b = cube
  return (y, z, x)

cubes.sort(key=zsort)

render(
  "render-4-3",
  cubes,
  1024,
  1024,
  2,
  40,
  20,
)