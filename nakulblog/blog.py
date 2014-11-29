import os
import re
import webapp2
import jinja2
import time

from string import letters

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class MainPage(Handler):

    def render_front(self, subject="", blog="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog "
                            "ORDER BY created DESC ")
        time.sleep(1)
        self.render("front.html", subject= subject, blog= blog, error = error, blogs = blogs)

    def get(self):
        self.render_front("front.html")


class FormPage(Handler):

    def get(self):
        self.render("form.html")

    def post(self):
        subject = self.request.get("subject")
        blog = self.request.get("blog")

        if subject and blog:
            b = Blog(subject = subject, blog = blog)
            b_key = b.put()

            self.redirect("/blog/%d" % b_key.id())
        else:
            error = "we need both a subject and a body"
            self.render(subject, blog, error)

class Permalink(MainPage):
        def get(self, blog_id):
            s = Blog.get_by_id(int(blog_id))
            self.render("front.html", blogs=[s])

app = webapp2.WSGIApplication([('/', MainPage),
                                ('/newpost', FormPage),
                                ('/blog/(\d+)', Permalink)
                               ],
                                debug = True)