import os

import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader =  jinja2.FileSystemLoader(template_dir), autoescape = True)






class Handler(webapp2.RequestHandler):

	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)	
	def render_str(self,template, **params):
		t= jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template,**kw))


class Data(db.Model):
	title= db.StringProperty(required = True)
	para= db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	

class MainPage(Handler):

	def render_front(self):
		data = db.GqlQuery("SELECT * FROM Data 	"
							"ORDER BY created DESC")
		self.render("page.html")

	def get(self):
		self.render_front()	
	
class newpost(Handler):
	def render_page(self, title="", para="",error=""):
		self.render("add.html" ,title = title , para = para , error = error)

	def get(self):
		self.render_page()
	def post(self):
		title= self.request.get("title")
		para=self.request.get("para")

		if title and para:
			a = Data(title= title, para=para) 
			a.put()
			self.redirect("/blog")
		else:
			error="we need both a title and para!"
			self.render_page(title, para, error)



app= webapp2.WSGIApplication([("/blog", MainPage),("/blog/newpost", newpost),
	], debug=True)	