import webapp2
import socialdataapp
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
            if profile:
                values['name'] = profile.name
        render_template(self, 'mainpageapp.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_user_data()
            profile = socialdataapp.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
                values['description'] = profile.description
            render_template(self, 'profile-edit.html', values)

class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            description = self.request.get('description')

            if len(name) < 2:
                error_text += 'Name should be at least 2 characters.\n'
            if len(name) > 20:
                error_text += 'Name should be no more than 20 characters.\n'
            if len(name.split()) > 1:
                error_text += 'Name should not have whitespace.\n'
            if len(description) > 4000:
                error_text += 'Description should be less than 4000 characters.\n'
            for word in description.split():
                if len(word) > 50:
                    error_text += 'Description contains words that are too damned long. \n'
                    break

            values = get_user_data()
            values['name'] = name
            values['description'] = description
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdataapp.save_profile(email, name,description)
                values['successmsg'] = 'Everything worked out fine.'
            render_template(self, 'profile-edit.html', values)

class ProfileViewHandler(webapp2.RequestHandler):
    def get(self, profilename):
        profile = socialdataapp.get_profile_by_name(profilename)
        values = get_user_data()
        values['name'] = 'Unknown'
        values['description'] = 'Profile does not exist.'
        if profile:
            values['name'] = profile.name
            values['description'] = profile.description
        render_template(self, 'profile-view.html', values) 

class ProfileListHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdataapp.get_recent_profiles()
        values = get_user_data()
        values['profiles'] = profiles
        render_template(self, 'profile-list.html', values)

app = webapp2.WSGIApplication([
    ('/profile-list', ProfileListHandler),
    ('/p/(.*)', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    ('.*', MainHandler),
])