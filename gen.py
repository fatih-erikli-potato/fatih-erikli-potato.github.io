from html import make_html_w_doctype, div
f = open("index.html", "w")
html = make_html_w_doctype(
  {"title": "Fatih Erikli", "stylesheet_url": "/style.css", "favicon_url": "/favicon.png"},
  div({"class": "container"}, "Homepage")
)
f.write(html)
f.close()