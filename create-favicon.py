import random
from png import dump_png
def px(x, y):
  return "{x}:{y}".format(x=x, y=y)
def draw(size, scr):
  out = []
  for y in range(0, size*2):
    row = []
    for x in range(0, size*2):
      row.append(scr.get(px(x - size, -1*(y - size)), (255, 255, 255)))
    out.append(row)
  return out
size = 64
scr = {}
for x in range(-64, 64):
  for y in range(-64, 65):
    scr[px(x, y)] = random.choice([[230,230,230], [255,255,255], [255,255,255], [255,255,255]])
png = draw(size, scr)
f = open("favicon.png", "wb")
dump_png(f, png)
f.close()