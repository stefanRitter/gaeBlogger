# GAE
import webapp2

from templates import *
from data import *


class BlogHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery('select * from Post order by created DESC')
        template = jinja_environment.get_template('blog.html')
        self.response.out.write(template.render({'posts': posts}))


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
            # todo: put in db and redirect to permalink
            post = Post(subject=title, content=content)
            post.put()
            self.redirect('/blog')
        else:
            error = "you must provide a subject and content"
            self.render_newpost(error, title, content)
