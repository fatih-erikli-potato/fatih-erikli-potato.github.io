from html import make_html_w_doctype, div, img
f = open("index.html", "w")
html = make_html_w_doctype(
  {"title": "Font Renderer", "favicon_url": "/favicon.png", "scripts": ["/font.js"]},
  div({"class": "container"})
)
f.write(html)
f.close()