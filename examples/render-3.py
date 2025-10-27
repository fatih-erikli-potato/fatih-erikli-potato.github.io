from render import render
from ball import create_ball
from bezier import bezier
import math

def makeid(x, y, z):
  return "{0}:{1}:{2}".format(x, y, z)

cubes = []
cubes_in_scene = set()

curve = [
  [-60, 0, -80],
  [0, 0, -80],
  [0, 0, 60],
  [60, 0, 60],
]

balls = 200
for i in range(0, balls):
  px, py, pz = bezier(i/balls, curve[0], curve[1], curve[2], curve[3])
  for x, y, z in create_ball(10):
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
  "render-3",
  cubes,
  512,
  512,
  4,
  40,
  20,
)