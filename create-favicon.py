import random
from png import dump_png
def px(x, y):
  return "{x}:{y}".format(x=x, y=y)
def draw(size, scr):
  out = []
  for y in range(0, size):
    row = []
    for x in range(0, size):
      row.append(scr.get(px(x, y), (255, 255, 255)))
    out.append(row)
  return out
size = 128
scr = {}
grid = 64
cellsize = int(size / grid)
cells = []
for y in range(grid):
  row = []
  for x in range(grid):
    row.append(random.choice([[230,230,230], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]))
  cells.append(row)
for row, cols in enumerate(cells):
  for col, cell in enumerate(cols):
    for x in range(0, cellsize):
      for y in range(0, cellsize):
        scr[px(col*cellsize+x, row*cellsize+y)] = cell
png = draw(size, scr)
f = open("favicon.png", "wb")
dump_png(f, png)
f.close()