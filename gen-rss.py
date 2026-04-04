from html import make_rss, title, link, description, item
from get_posts import get_posts

posts = get_posts(preview=True)

items_tags = []
for post in posts:
  items_tags.append(
    item(
      title(post["title"]),
      link("https://fatih-erikli-potato.github.io/blog/{0}".format(post["slug"])),
      description(post["description"])
    )
  )

rss_text = make_rss(
  title("Fatih Erikli's notes on computer graphics"),
  link("a https://fatih-erikli-potato.github.io"),
  description("My notes on computer graphics"),
  *items_tags
)

with open("rss.xml", "w") as f:
  f.write(rss_text)