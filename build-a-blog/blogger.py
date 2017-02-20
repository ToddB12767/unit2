import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
jinja_environment=jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
	subject= db.StringProperty(required=True)
	content= db.TextProperty (required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("post.html", p = self)


class Blog(BlogHandler):

	def write_Blog (self):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5"  )
		error_message=self.error
		template = jinja_environment.get_template('blog.html')
		template_values = {
		'posts': posts
        }

		self.response.write(template.render(template_values))

	def get(self):
		self.write_Blog()

class NewPost(BlogHandler):

	def write_newPost (self,last="",entryName="",entry="", error=""):
		error_message=self.error
		template = jinja_environment.get_template('newPost.html')
		template_values = {
			'entryName':entryName,
			'entry': entry,
			'error': error
        }

		self.response.write(template.render(template_values))

	def get(self):
		self.write_newPost()

	def post(self):
		subject=self.request.get("subject")
		content=self.request.get("content")
		if subject and content:
			p= Post(parent= blog_key(),subject= subject, content= content)
			p.put()
			self.redirect('/blog/%s' % str(p.key().id()))
		else:
			self.write_newPost(entryName=subject,entry=content,error="Please enter a title and text to submit a new blog entry")


class PostPage(BlogHandler):

	def get(self, post_id):
		key= db.Key.from_path("Post", int(post_id), parent=blog_key())
		post= db.get(key)

		if not post:
			self.error(404)
			return

		self.render("permalink.html", post = post)
