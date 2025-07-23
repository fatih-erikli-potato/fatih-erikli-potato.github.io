from html import make_html_w_doctype, div, img
from PIL import Image
import os
f = open("index.html", "w")
heading = []
heading_text = "Fatih Erikli"
texts_div = []
texts = [
"The dog in left is an award winning showdog named Arnie an AKC French Bulldog. The dog on the right is Flint, bred in Netherlands by hawbucks French bulldog, a breeder trying to establish a new, healtier template for French Bulldogs.",
"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
"Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of de Finibus Bonorum et Malorum, The Extremes of Good and Evil by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, Lorem ipsum dolor sit amet.., comes from a line in section 1.10.32."
]
for words_text in texts:
  words = []
  scale = 0.01
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
  texts_div.append(div(div({"class": "hide-text"}, words_text), *words))
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
  {"title": "Fatih Erikli", "favicon_url": "favicon.png",
  "styles": ["style.css"],
  "scripts": []},
  div({"class": "container"},
    div(div({"class": "hide-text"}, heading_text), *heading), *texts_div),
  div({"class": "render"},
    #img({"src": "rakowicka.png", "width": "512px", "height": "512px"}),
    #img({"src": "rakowicka-2x.png", "width": "512px", "height": "512px"}),
    img({"src": "cup-of-coffee.png", "width": "512px", "height": "512px"}),
  )
)
f.write(html)
f.close()