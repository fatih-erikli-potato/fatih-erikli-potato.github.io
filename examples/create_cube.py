def create_cube(x, y, z, rotate_horizontal, rotate_vertical):
  # only up to horizontally 90 degrees implemented in this example
  if rotate_vertical > 0 and rotate_vertical < 90 and rotate_horizontal < 90 and rotate_horizontal > 0:
    return [
      [
        20, # this is in percent
        [x+0.5, y+0.5, z-0.5],
        [x+0.5, y+0.5, z+0.5],
        [x+0.5, y-0.5, z+0.5],
        [x+0.5, y-0.5, z-0.5]
      ],
      [
        5,
        [x-0.5, y+0.5, z-0.5],
        [x+0.5, y+0.5, z-0.5],
        [x+0.5, y+0.5, z+0.5],
        [x-0.5, y+0.5, z+0.5]
      ],
      [
        30,
        [x-0.5, y+0.5, z+0.5],
        [x+0.5, y+0.5, z+0.5],
        [x+0.5, y-0.5, z+0.5],
        [x-0.5, y-0.5, z+0.5]
      ]
    ]