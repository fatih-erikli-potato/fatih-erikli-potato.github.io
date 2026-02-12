from PIL import Image
import os
directory = "monospace"
for filename in os.listdir(directory):
  if not filename.endswith(".png"):
    continue
  filepath = os.path.join(directory, filename)
  image = Image.open(filepath)
  width, height = image.size
  square = int(width/20)
  for x in range(0, width):
    for y in range(0, height):
      r, g, b, a = image.getpixel((x, y))
      if a == 0:
        r, g, b, a = 240, 240, 240, 255
      else:
        r, g, b, a = 0, 0, 0, 0
      image.putpixel((x, y), (r, g, b, a))
  image.save(os.path.join("monospace-masked", filename))
