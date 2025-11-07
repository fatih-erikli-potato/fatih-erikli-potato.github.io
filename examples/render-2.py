from render import render
from ball import create_ball

cubes = []

for x, y, z in create_ball(128):
 cubes.append([x, y, z, 255, 255, 255])

render(
  "render-2-1",
  cubes,
  1024,
  1024,
  4,
  40,
  20,
)