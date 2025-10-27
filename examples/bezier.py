def lerp(t, a, b):
  ax, ay, az = a
  bx, by, bz = b
  dx = bx - ax
  dy = by - ay
  dz = bz - az
  return [ax + t * dx, ay + t * dy, az + t * dz]
 
def bezier(t, p0, p1, p2, p3):
  a = lerp(t, p0, p1)
  b = lerp(t, p1, p2)
  c = lerp(t, p2, p3)
  d = lerp(t, a, b)
  e = lerp(t, b, c)
  f = lerp(t, d, e)
  return f