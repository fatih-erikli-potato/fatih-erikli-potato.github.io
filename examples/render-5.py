from render import render
from ball import create_ball
from bezier import bezier, lerp

def distance(a, b):
  ax, ay, az = a
  bx, by, bz = b
  dx = max(ax, bx) - min(ax, bx)
  dy = max(ay, by) - min(ay, by)
  dz = max(az, bz) - min(az, bz)
  # the longest distance of axises will be used for interpolating the line
  # between a and b. no square root calculation needed here.
  return max(dx, dy, dz)

cubes = []

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
ball_size = 2

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
    px, py, pz = bezier(f/fall, wa, wb, wc, wd)
    for x, y, z in create_ball(ball_size):
      cubes.append([px + x, py + y, pz + z, 255, 255, 255])
    a = bezier(f/fall, wa, wb, wc, wd)
    b = bezier(f/fall, wa_next, wb_next, wc_next, wd_next)
    c = bezier((f+1)/fall, wa_next, wb_next, wc_next, wd_next)
    d = bezier((f+1)/fall, wa, wb, wc, wd)

    segments_wide = max(distance(a,b), distance(d, c))
    for i in range(0, int(segments_wide)):
      linea = lerp(i/segments_wide, a, b)
      lineb = lerp(i/segments_wide, d, c)
      segments_line = distance(linea, lineb)
      for j in range(0, int(segments_line)):
        px, py, pz = lerp(j/segments_line, linea, lineb)
        for x, y, z in create_ball(ball_size):
          cubes.append([px + x, py + y, pz + z, 255, 255, 255])

def zsort(cube):
  x, y, z, r, g, b = cube
  return (y, z, x)

cubes.sort(key=zsort)

render(
  "render-5",
  cubes,
  1024,
  1024,
  2,
  40,
  20,
)