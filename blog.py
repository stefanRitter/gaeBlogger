
import webapp2
import time

from google.appengine.api import memcache

from templates import *
from data import *

# blog memcache key
key = 'blogmain'


# load posts from memcache or DB if necessary
def load_posts(update=False):
    posts = memcache.get(key)

    if posts is None or update:
        posts = db.GqlQuery('select * from Post order by created DESC')
        posts = list(posts)
        memcache.set(key, posts)
        memcache.set('time', time.time())

    return posts, memcache.get('time')


# load individual post from memcache or DB if necessary
def load_post(post_id, update=False):
    posts = memcache.get(key)

    for p in posts:
        if str(p.key().id()) == post_id:
            return p, memcache.get('time')

    return Post.get_by_id(int(post_id)), 0


# blog and post handlers
class BlogHandler(webapp2.RequestHandler):
    def get(self):
        posts = load_posts()
        template = jinja_environment.get_template('blog.html')
        self.response.out.write(template.render({'posts': posts[0], 'timestamp': int(time.time() - posts[1])}))


class PostHandler(webapp2.RequestHandler):
    def get(self, post_id):
        post = load_post(post_id)
        template = jinja_environment.get_template('post.html')

        if post:
            self.response.out.write(template.render({'post': post[0], 'timestamp': int(time.time() - post[1])}))
        else:
            self.redirect('/blog')


class NewPostHandler(webapp2.RequestHandler):
    def render_newpost(self, error="", subject="", content=""):
        template = jinja_environment.get_template('newpost.html')
        self.response.out.write(template.render({'subject': subject, 'content': content, 'error': error}))

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get('subject')
        content = self.request.get('content')

        if title and content:
            post = Post(subject=title, content=content)
            post.put()
            load_posts(True)  # update memcache
            key = str(post.key().id())  # get id and convert to string
            self.redirect('/blog/%s' % key)
        else:
            error = "you must provide a subject and content"
            self.render_newpost(error, title, content)


# flush memcache
class FlushHandler(webapp2.RequestHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/')
