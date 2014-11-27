import os
import webapp2
import jinja2
import time
import urllib2
from xml.dom import minidom

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

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    ip = "4.2.2.2"
    ip = "23.24.209.141"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return

    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

gmaps_url = "https://maps.googleapis.com/maps/api/staticmap?size=380x260&sensor=false&"

def gmaps_img(points):
        markers = '&'.join("markers=%s,%s" % (p.lat, p.lon) for p in points)
        return gmaps_url + markers

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

class MainPage(Handler):

    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                            "ORDER BY created DESC ")
        arts = list(arts) #prevents running of  multiple queries. Local copy of datastore to access as much as you want available now/
        points = []
        for a in arts:
            if a.coords:
                points.append(a.coords)
        img_url = None
        if points:
            img_url = gmaps_img(points)

        time.sleep(1)
        self.render("front.html", title= title, art= art, error = error, arts = arts, img_url = img_url)


    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            #lookup coordinates add to art
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords

            a.put()

            self.redirect("/")
        else:
            error = "we need both a title and an art"
            self.render_front(title, art, error)


app = webapp2.WSGIApplication([('/', MainPage),
                               ],
                                debug = True)