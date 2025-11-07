def create_ball(r, origin_x=0, origin_y=0, origin_z=0):
  ball = []
  for x in range(-r, r):
    for y in range(-r, r):
      for z in range(-r, r):
        if x**2 + y**2 + z**2 < r**2:
          ball.append([origin_x + x, origin_y + y, origin_z + z])
  return ball