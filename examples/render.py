from create_cube import create_cube
from darken import darken
from rotate import rotate_xyz
 
from PIL import Image, ImageDraw
 
def render(name, cubes, width, height, unit_scale, rotate_horizontal, rotate_vertical, save=True):
  width *= unit_scale
  height *= unit_scale
  image = Image.new("RGB", (width, height), (255, 255, 255))
  draw = ImageDraw.Draw(image)
  for x, y, z, r, g, b in cubes:
    cube = create_cube(x, y, z, rotate_horizontal, rotate_vertical)
    for darken_percent, *diamond in cube:
      points = []
      for xx, yy, zz in diamond:
        xn, yn, zn = rotate_xyz(xx * unit_scale, yy * unit_scale, zz * unit_scale, rotate_horizontal, rotate_vertical)
        x = width/2 + xn
        y = height/2 + (yn * -1)
        points.append((x, y))
      draw.polygon(points, darken(r, g, b, darken_percent))
  if save:
    image.save(open("{}.png".format(name), "wb"), "PNG")
  return image