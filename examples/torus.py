from render import render
from ball import create_ball
from bezier import bezier
from rotate import rotate
import math

cubes = []

scale = 2
radius = 25 * scale
radius_penne_ball = 5 * scale
penne_half_long = 110 * scale
penne_cut = 30
sticks = 18

penne = []
penne_set = set()

for z in range(-penne_half_long, penne_half_long):
  penne_ball = create_ball(radius_penne_ball, 0, radius, z)
  for xyz in penne_ball:
    penne.append(xyz)

penne_piece = []

for deg in range(0, 360, int(360/sticks)):
  for (x, y, z) in penne:
    xrotated, yrotated = rotate(x, y, deg)
    
    _, zrotated = rotate(yrotated, z, penne_cut)
    if zrotated < penne_half_long - penne_cut and zrotated > -penne_half_long + penne_cut:
      penne_piece.append([xrotated, yrotated, z])

for x, y, z in penne_piece:
  cubes.append([x, y, z, 255, 255, 200])

def zsort(cube):
  x, y, z, r, g, b = cube
  return (y, z, x)

cubes.sort(key=zsort)

render(
  "torus",
  cubes,
  1024,
  1024,
  4,
  40,
  20,
)