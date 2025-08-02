from html import make_html_w_doctype, div, img, a, iframe
from syntax_highlighter import tokenize
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

def get_text_block(text, scale, dir_="glyph"):
  imgs = []
  fish = {"elements": [], "w": 0}
  fishes = [fish]
  for w in text:
    if w == " ":
      glyphname = "space"
    else:
      glyphname = "{0}".format(ord(w))
    glyph_png_relative_path = "{0}/draft-{1}.png".format(dir_, glyphname)
    pngf = Image.open(glyph_png_relative_path)
    wid = pngf.size[0]*scale
    fish["w"] += int(wid)
    imgattrs = {
      "width": "{0}px".format(int(wid)),
      "height": "{0}px".format(int(pngf.size[1]*scale)),
      "alt": w,
      "src": glyph_png_relative_path}
    fish["elements"].append(img(imgattrs))
    if w == " ":
      fish = {"elements": [], "w": 0}
      fishes.append(fish)
  fish_block = []
  for fish in fishes:
    fish_block.append(div({"style": {"width": "{0}px".format(int(fish["w"]))}}, *fish["elements"]))
  return div({"class": "text-block"}, *fish_block)

def get_code_line_block(text, scale, tokens, line_starts_at):
  imgs = []
  fish = {"elements": [], "w": 0}
  fishes = [fish]
  i = 0
  for w in text:
    if w == " ":
      glyphname = "space"
    else:
      glyphname = "{0}".format(ord(w))
    glyph_png_relative_path = "monospace-masked/draft-{0}.png".format(glyphname)
    pngf = Image.open(glyph_png_relative_path)
    wid = pngf.size[0]*scale
    token = seek_token_by_char_index(tokens, line_starts_at + i)
    fish["w"] += int(wid)
    imgattrs = {
      "class": ["masked"],
      "width": "{0}px".format(int(wid)),
      "height": "{0}px".format(int(pngf.size[1]*scale)),
      "alt": w,
      "src": glyph_png_relative_path}
    if token:
      imgattrs["class"].append(token["type"])
    fish["elements"].append(img(imgattrs))
    if w == " ":
      fish = {"elements": [], "w": 0}
      fishes.append(fish)
    i += 1
  fish_block = []
  for fish in fishes:
    fish_block.append(div({"style": {"width": "{0}px".format(int(fish["w"]))}}, *fish["elements"]))
  return div({"class": "code-block"}, *fish_block)

def seek_token_by_char_index(tokens, char_index):
  for token in tokens:
    if char_index >= token["starts"] and char_index < token["ends"]:
      return token

def get_code_block(text, scale):
  tokens = tokenize(text)
  ps = []
  line_starts_at = 0
  for line in text.split("\n"):
    ps.append(get_code_line_block(line, scale, tokens, line_starts_at))
    line_starts_at += len(line) + 1
  return ps

def get_text_paragraphs(text, scale):
  ps = []
  paragraphs = text.split("\n")
  seek_code = False
  
  index_at_text = 0
  code = ""
  for paragraph in paragraphs:
    if paragraph == "- code -":
      if seek_code:
        ps.extend(get_code_block(code, scale))
        seek_code = False
        code = ""
      else:
        seek_code = True
      continue
    else:
      if seek_code:
        code += paragraph + "\n"
      else:
        ps.append(get_text_block(paragraph, scale))
    index_at_text += len(paragraph) + 1
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
    div({"class": "text-block"},
      a({"href": "{0}.html".format(post["slug"])}, *get_text(post["title"], 0.01))
    )
  )
write_html("index.html", "THINKING OUT LOUD", div(
  div({"class": "header"}, *get_text("HI, I AM FATIH ERIKLI", 0.02)),
  div({"class": "text-block"}, *get_text("I am a software developer.", 0.01)),
  div({"class": "header"}, *get_text("THINKING OUT LOUD", 0.02)),
  *posts_tags,
))
for post in posts:
  write_html("{0}.html".format(post["slug"]), post["title"],
    div({"class": "text-block"}, a({"href": "/"}, *get_text("home", 0.01))),
    div({"class": "header"}, *get_text(post["title"], 0.02)),
    *get_text_paragraphs(post["content"], 0.01)
  )
