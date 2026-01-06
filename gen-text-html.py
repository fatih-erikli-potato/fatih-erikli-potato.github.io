from html import make_html_w_doctype, div, img
f = open("text.html", "w")
html = make_html_w_doctype(
  {"title": "Font Renderer", "favicon_url": "favicon.png",
  "styles": ["style.css"],
  "scripts": ["font-text.js"]},
  div({"class": "container"})
)
f.write(html)
f.close()