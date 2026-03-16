def create_cube(x, y, z, rotate_horizontal, rotate_vertical):
  # only up to horizontally 90 degrees implemented in this example
  if rotate_vertical > 0 and rotate_vertical < 90 and rotate_horizontal < 90 and rotate_horizontal > 0:
    return [
      [
        20, # this is in percent
        [x, y, z-1],
        [x, y, z],
        [x, y-1, z],
        [x, y-1, z-1]
      ],
      [
        5,
        [x-1, y, z-1],
        [x, y, z-1],
        [x, y, z],
        [x-1, y, z]
      ],
      [
        30,
        [x-1, y, z],
        [x, y, z],
        [x, y-1, z],
        [x-1, y-1, z]
      ]
    ]