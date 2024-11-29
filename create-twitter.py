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
size = 2048
scr = {}
grid = 128
cellsize = int(size / grid)
cells = []
for y in range(grid):
  row = []
  for x in range(grid):
    row.append(random.choice([[220,220,220], [245, 245, 245], [245, 245, 245], [245, 245, 245], [245, 245, 245]]))
  cells.append(row)
for row, cols in enumerate(cells):
  for col, cell in enumerate(cols):
    for x in range(0, cellsize):
      for y in range(0, cellsize):
        scr[px(col*cellsize+x, row*cellsize+y)] = cell
png = draw(size, scr)
f = open("twitter.png", "wb")
dump_png(f, png)
f.close()