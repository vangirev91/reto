from datetime import datetime
from instaloader import Instaloader, Post


L = Instaloader()
post = Post.from_shortcode(L.context, "B166OkVBPJR")
print(post.get_comments())

from datetime import datetime
from instaloader import Instaloader, Post


L = Instaloader()
post = Post.from_shortcode(L.context, "B166OkVBPJR")
print(post.get_comments())

