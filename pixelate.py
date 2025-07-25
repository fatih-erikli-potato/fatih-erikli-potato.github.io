from PIL import Image
import os
directory = "glyph"
def avgrgb(image, xstart, ystart, square):
  sumr = 0
  sumg = 0
  sumb = 0
  for x in range(xstart, xstart+square):
    for y in range(ystart, ystart+square):
      r, g, b = image.getpixel((x, y))
      sumr += r
      sumg += g
      sumb += b
  return (
    int(sumr / square**2),
    int(sumg / square**2),
    int(sumb / square**2),
  )
def putrgbsquare(image, xstart, ystart, square, rgb):
  for x in range(xstart, xstart+square):
    for y in range(ystart, ystart+square):
      image.putpixel((x, y), rgb)
for filename in os.listdir(directory):
  if not filename.endswith(".png"):
    continue
  filepath = os.path.join(directory, filename)
  image = Image.open(filepath)
  width, height = image.size
  square = 120
  for x in range(0, width-square, square):
    for y in range(0, height-square, square):
      r, g, b = avgrgb(image, x, y, square)
      if (r + g + b)/3 < 200:
        r, g, b = 0, 0, 0
      else:
        r, g, b = 255, 255, 255
      putrgbsquare(image, x, y, square, (r, g, b))
  image.save(os.path.join("out", filename))
