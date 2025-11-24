from create_cube import create_cube
from xyz_on_canvas import xyz_on_canvas
from darken import darken
 
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
        x, y = xyz_on_canvas(xx, yy, zz, unit_scale, width, height, rotate_horizontal, rotate_vertical)
        points.append((x, y))
      draw.polygon(points, darken(r, g, b, darken_percent))
  if save:
    image.save(open("{}.png".format(name), "wb"), "PNG")
  return image