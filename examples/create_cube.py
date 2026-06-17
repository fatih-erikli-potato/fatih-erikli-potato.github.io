def create_cube(x, y, z, rotate_horizontal, rotate_vertical):
  if rotate_vertical > 0 and rotate_vertical < 90 and rotate_horizontal < 90 and rotate_horizontal > 0:
    return [
      [
        20, # this is in percent
        [x+1, y, z],
        [x+1, y, z+1],
        [x+1, y-1, z+1],
        [x+1, y-1, z]
      ],
      [
        5,
        [x, y, z],
        [x+1, y, z],
        [x+1, y, z+1],
        [x, y, z+1]
      ],
      [
        25,
        [x, y, z+1],
        [x+1, y, z+1],
        [x+1, y-1, z+1],
        [x, y-1, z+1]
      ]
    ]