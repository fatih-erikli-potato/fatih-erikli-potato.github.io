def create_ball(r):
  ball = []
  for x in range(-r, r):
    for y in range(-r, r):
      for z in range(-r, r):
        if x**2 + y**2 + z**2 < r**2:
          ball.append([x, y, z])
  return ball