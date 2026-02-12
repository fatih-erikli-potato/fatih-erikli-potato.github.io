from rotate import rotate_xyz

def xyz_on_canvas(x, y, z, unit_scale, w, h, rh, rv, include_z=False):
  xn, yn, zn = rotate_xyz(x * unit_scale, y * unit_scale, z * unit_scale, rh, rv)
  x_on_canvas = w/2 + xn
  y_on_canvas = h/2 + (yn * -1)
  if include_z:
    return (x_on_canvas, y_on_canvas, zn)
  return (x_on_canvas, y_on_canvas)