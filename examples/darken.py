def darken(r, g, b, percent):
  rblacks = int(r * (percent/100))
  gblacks = int(g * (percent/100))
  bblacks = int(b * (percent/100))
  return (r - rblacks, g - gblacks, b - bblacks)