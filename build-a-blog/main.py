import os
import webapp2
import jinja2
import blogger
from google.appengine.ext import db

jinja_environment=jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))


class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.write(template.render())

class Resume(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('resume.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([('/', MainHandler),
							('/resume',Resume),
							('/blog',blogger.Blog),
							('/newpost',blogger.NewPost),
							('/blog/newpost',blogger.NewPost),
							('/blog/([0-9]+)', blogger.PostPage)
							],
							 debug=True)
