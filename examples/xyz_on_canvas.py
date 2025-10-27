from rotate import rotate_xyz

def xyz_on_canvas(x, y, z, unit_scale, w, h, rh, rv):
  xn, yn, zn = rotate_xyz(x * unit_scale, y * unit_scale, z * unit_scale, rh, rv)
  return (int(w/2+xn), int(h/2+(yn*-1)))