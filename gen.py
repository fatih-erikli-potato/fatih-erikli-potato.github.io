from html import make_html_w_doctype, div, img
f = open("index.html", "w")
html = make_html_w_doctype(
  {"title": "Font Renderer", "favicon_url": "favicon.png",
  "styles": ["style.css"],
  "scripts": ["font.js"]},
  div({"class": "container"}),
  div({"class": "render"},
    #img({"src": "rakowicka.png", "width": "512px", "height": "512px"}),
    #img({"src": "rakowicka-2x.png", "width": "512px", "height": "512px"}),
    img({"src": "cup-of-coffee.png", "width": "512px", "height": "512px"}),
  )
)
f.write(html)
f.close()