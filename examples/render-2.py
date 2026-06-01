from render import render
from ball import create_ball

cubes = []

for x, y, z in create_ball(128):
 cubes.append([x, y, z, 255, 255, 255])

def zsort(cube):
  x, y, z, r, g, b = cube
  return (y, z, x)

cubes.sort(key=zsort)

render(
  "render-2-1",
  cubes,
  1024,
  1024,
  4,
  40,
  20,
)