from rotate import rotate_xyz
 
from PIL import Image, ImageDraw
 
def carboncopy(abcd, width, height, unit_scale, rotate_horizontal, rotate_vertical):
  width *= unit_scale
  height *= unit_scale
  image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
  draw = ImageDraw.Draw(image)
  points = []
  for xx, yy, zz in abcd:
    xn, yn, zn = rotate_xyz(xx * unit_scale, yy * unit_scale, zz * unit_scale, rotate_horizontal, rotate_vertical)
    x = width/2 + xn
    y = height/2 + (yn * -1)
    points.append((x, y))
  draw.polygon(points, (0, 0, 0, 255))
  return image