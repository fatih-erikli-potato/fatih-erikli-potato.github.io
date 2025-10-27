def create_cube(x, y, z, rotate_horizontal, rotate_vertical):
  # the cube will be drawn in a square form if the scenery is in two-dimension
  if rotate_vertical == 0 and rotate_horizontal == 0:
    return [
      [
        0,
        # this value is the darkening amount of shape.
        # the color will stay as it is in two-d.
        [x-0.5, y+0.5, z+0.5],
        [x+0.5, y+0.5, z+0.5],
        [x+0.5, y-0.5, z+0.5],
        [x-0.5, y-0.5, z+0.5],
      ]
    ]
  # only up to horizontally 90 degrees implemented in this example
  if rotate_vertical > 0 and rotate_vertical < 90 and rotate_horizontal < 90 and rotate_horizontal > 0:
    return [
      [
        20,
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