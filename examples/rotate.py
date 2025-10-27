import math

def rotate(x, y, deg):
  cos = math.cos(math.radians(deg))
  sin = math.sin(math.radians(deg))
  return [cos * x - sin * y, cos * y + sin * x]
 
def rotate_xyz(x, y, z, rh, rv):
  xn, zn = rotate(x, z, rh)
  yn, zn = rotate(y, zn, rv)
  return [xn, yn, zn]