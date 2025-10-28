from PIL import Image
import os

directory = "monospace-masked"
target = "monospace-masked-resized"

resize = 0.2

for filename in os.listdir(directory):
  if not filename.endswith(".png"):
    continue
  filepath = os.path.join(directory, filename)
  image = Image.open(filepath)
  width, height = image.size
  image = image.resize((int(width*resize), int(height*resize)))
  image.save(os.path.join(target, filename))
