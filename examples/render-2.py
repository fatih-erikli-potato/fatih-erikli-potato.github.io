from render import render
from ball import create_ball

cubes = []

for x, y, z in create_ball(16):
 cubes.append([x, y, z, 255, 255, 255])

render(
  "render-2",
  cubes,
  128,
  128,
  16,
  40,
  20,
)