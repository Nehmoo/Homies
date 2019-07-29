import webapp2
import socialdata
from google.appengine.ext.webapp import template
import os
from google.appengine.api import users

def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))

def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None

def get_user_data():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_user_data()
        if get_user_email():
            profile = socialdataapp.get_user_profile(get_user_email())
            values['name'] = profile.name
        render_template(self, 'mainpageapp.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_user_data()
            profile = socialdata.get_user_profile(get_user_email())
            values['name'] = profile.name
            values['description'] = profile.description
            render_template(self, 'profile-edit.html', values)

app = webapp2.WSGIApplication([
    ('/profile-edit', ProfileEditHandler),
    ('.*', MainHandler),
])