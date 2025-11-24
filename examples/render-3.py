from render import render
from ball import create_ball
from bezier import bezier

cubes = []

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
    cubes.append([px + x, py + y, pz + z, 255, 255, 255])

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