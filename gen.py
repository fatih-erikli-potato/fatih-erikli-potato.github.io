from html import make_html_w_doctype, div, img, a
from PIL import Image
import os
def get_text(text, scale):
  imgs = []
  for w in text:
    if w == " ":
      glyphname = "space"
    else:
      glyphname = "{0}".format(ord(w))
    glyph_png_relative_path = "glyph/draft-{0}.png".format(glyphname)
    pngf = Image.open(glyph_png_relative_path)
    imgs.append(img({
      "width": "{}".format(int(pngf.size[0]*scale)),
      "height": "{}".format(int(pngf.size[1]*scale)),
      "alt": w,
      "src": glyph_png_relative_path}))
  return imgs

def get_text_block(text, scale):
  imgs = []
  fish = {"elements": [], "w": 0}
  fishes = [fish]
  for w in text:
    if w == " ":
      glyphname = "space"
    else:
      glyphname = "{0}".format(ord(w))
    glyph_png_relative_path = "glyph/draft-{0}.png".format(glyphname)
    pngf = Image.open(glyph_png_relative_path)
    wid = pngf.size[0]*scale
    fish["w"] += wid
    fish["elements"].append(img({
      "width": "{0}px".format(int(wid)),
      "height": "{0}px".format(int(pngf.size[1]*scale)),
      "alt": w,
      "src": glyph_png_relative_path}))
    if w == " ":
      fish = {"elements": [], "w": 0}
      fishes.append(fish)
  fish_block = []
  for fish in fishes:
    fish_block.append(div({"width": "{0}px".format(int(fish["w"]))}, *fish["elements"]))
  return div({"class": "text-block"}, *fish_block)

def get_text_paragraphs(text, scale):
  ps = []
  paragraphs = text.split("\n")
  for paragraph in paragraphs:
    ps.append(get_text_block(paragraph, scale))
  return ps

def get_posts():
  f = open("thoughts", "r")
  posts_d = f.read()
  f.close()
  posts = []
  posts_d_split = posts_d.split("\n----\n")
  for post_raw in posts_d_split:
    first_breakline = post_raw.index("\n")
    second_breakline = post_raw.index("\n", first_breakline+1)
    title = post_raw[:first_breakline]
    slug = post_raw[first_breakline+1:second_breakline]
    content = post_raw[second_breakline+1:]
    posts.append({"title": title, "slug": slug, "content": content})
  return posts

def write_html(filename, title, *content):
  html = make_html_w_doctype(
    {"title": title, "favicon_url": "favicon.png",
    "styles": ["style.css"],
    "scripts": []},
    div({"class": "container"}, *content),
  )
  with open(filename, "w") as f:
    f.write(html)

posts = []
posts = get_posts()
posts_tags = []
for post in posts:
  posts_tags.append(
    div(
      a({"href": "{0}.html".format(post["slug"])}, *get_text(post["title"], 0.01))
    )
  )
write_html("index.html", "THINKING OUT LOUD", div(
  div({"class": "header"}, *get_text("THINKING OUT LOUD", 0.02)),
  *posts_tags,
))
for post in posts:
  write_html("{0}.html".format(post["slug"]), post["title"],
    a({"href": "/"}, *get_text("home", 0.01)),
    div({"class": "header"}, *get_text(post["title"], 0.02)),
    *get_text_paragraphs(post["content"], 0.01)
  )
