from html import make_html_w_doctype, div, img
from PIL import Image
import os
f = open("index.html", "w")
heading = []
heading_text = "Fatih Erikli"
words = []
words_text = "I am a software developer. I am from Karabük. Benim adım Fatih. Karabük'te yaşıyorum."
scale = 0.011
for w in words_text:
  if w == " ":
    glyphname = "space"
  else:
    glyphname = ord(w)
  glyph_png_relative_path = "glyph/draft-{0}.png".format(glyphname)
  pngf = Image.open(glyph_png_relative_path)
  words.append(img({
    "width": "{}".format(pngf.size[0]*scale),
    "height": "{}".format(pngf.size[1]*scale),
    "alt": w,
    "src": glyph_png_relative_path}))
scale = 0.02
for w in heading_text:
  if w == " ":
    glyphname = "space"
  else:
    glyphname = ord(w)
  glyph_png_relative_path = "glyph/draft-{0}.png".format(glyphname)
  pngf = Image.open(glyph_png_relative_path)
  heading.append(img({
    "width": "{}".format(pngf.size[0]*scale),
    "height": "{}".format(pngf.size[1]*scale),
    "alt": w,
    "src": glyph_png_relative_path}))
html = make_html_w_doctype(
  {"title": "Font Renderer", "favicon_url": "favicon.png",
  "styles": ["style.css"],
  "scripts": []},
  div({"class": "container"},
    div(*heading), div(*words)),
  div({"class": "render"},
    #img({"src": "rakowicka.png", "width": "512px", "height": "512px"}),
    #img({"src": "rakowicka-2x.png", "width": "512px", "height": "512px"}),
    img({"src": "cup-of-coffee.png", "width": "512px", "height": "512px"}),
  )
)
f.write(html)
f.close()