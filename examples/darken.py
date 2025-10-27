def darken(r, g, b, percent):
  rblacks = int(r * (percent/100))
  gblacks = int(g * (percent/100))
  bblacks = int(b * (percent/100))
  return (max(r - rblacks, 0), max(g - gblacks, 0), max(b - bblacks, 0))