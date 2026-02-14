from html import make_html_w_doctype, div, img, a, pre, span, p
from syntax_highlighter import tokenize
from PIL import Image
import os

class keygetter(dict):
  def __getitem__(self, key):
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, key)
    return open(filepath, "r").read()

def get_code_block(text, scale):
  tokens = tokenize(text)
  html_output = []
  for token in tokens:
    html_output.append(span({"class": token["type"]}, text[token["starts"]: token["ends"]]))
  return pre(*html_output)

def get_text_paragraphs(text, scale):
  ps = []
  text = (text % keygetter())
  paragraphs = text.split("\n")
  seek_code = False

  code = ""
  for paragraph in paragraphs:
    if paragraph.startswith("image:"):
      path = paragraph[len("image:"):]
      ps.append(div({"class": "image-block"}, img({
        "width": 512,
        "height": 512,
        "alt": path,
        "src": path
      })))
    elif paragraph == "- code -":
      if seek_code:
        ps.append(get_code_block(code, scale))
        seek_code = False
        code = ""
      else:
        seek_code = True
    else:
      if seek_code:
        code += paragraph + "\n"
      else:
        ps.append(p(paragraph))
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
    {"title": title, "favicon_url": "/favicon.png",
    "styles": ["/style-plain.css"],
    "scripts": []},
    div({"class": "container"}, *content,
      div({"class": "footer"},
        a({"href": "https://instagram.com/fatiherikli9278"}, "instagram"), " ",
        a({"href": "https://linkedin.com/in/fatih-erikli-2a8315337"}, "linkedin")
      )
    ),
  )
  with open(filename, "w") as f:
    f.write(html)

posts = []
posts = get_posts()
posts_tags = []
for post in posts:
  posts_tags.append(
    div({"class": "text-block"},
      a({"href": "blog/{0}.html".format(post["slug"])}, post["title"])
    )
  )
write_html("index.html", "THINKING OUT LOUD", div(
  div({"class": "header"}, "HI, I AM FATIH ERIKLI"),
  div({"class": "text-block"}, "I am a software developer"),
  div({"class": "header"}, "THINKING OUT LOUD"),
  *posts_tags
))
for post in posts:
  write_html("blog/{0}.html".format(post["slug"]), post["title"],
    div({"class": "text-block"}, a({"href": "/"}, "home")),
    div({"class": "header"}, post["title"]),
    *get_text_paragraphs(post["content"], 0.05)
  )
