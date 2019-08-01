import webapp2
import logging
import socialdataapp
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail


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
                values['user_contacts']= profile.user_contacts
            else:
                create_user_profile(get_user_email())
                
        render_template(self, 'mainpageapp.html', values)

    def post(self):
        from_address = 'anything@yeetbruh.appspotmail.com'
        email = self.request.get('email')
        mail.send_mail(from_address, email, 'Kisses', 'Your homie has just sent you a kiss!')
        values = get_user_data()
        values['message'] = 'The kiss has been sent.'
        render_template(self, 'messagesent.html', values)


class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_user_data()
            profile = socialdataapp.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
                values['description'] = profile.phone_number
          
                render_template(self, 'profile-edit.html', values)


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            phone_number = self.request.get('phone_number')
            if len(name) < 2:
                error_text += 'Name should be at least 2 characters.\n'
            if len(name) > 20:
                error_text += 'Name should be no more than 20 characters.\n'
            if len(name.split()) > 1:
                error_text += 'Name should not have whitespace.\n'
            if len(phone_number) > 10:
                error_text += 'Description should be less than 4000 characters.\n'
            for word in phone_number.split():
                if len(word) > 10:
                    error_text += 'Phone number too long. \n'
                    break
            email = self.request.get('email')
            phone_number = self.request.get('phonenumber')
            values = get_user_data()
            values['name'] = name
            values['email'] = email
            values['phonenumber'] = int(phone_number)
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdataapp.save_contact(get_user_email(), email, name, phone_number)
                values['successmsg'] = 'Everything worked out fine.'
            render_template(self, 'profile-save.html', values)


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





class FormHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        message = self.request.get('message')
        email = self.request.get('email')

        params = {
          'name': name,
          'message': message,
          'email': email
        }


app = webapp2.WSGIApplication([
    ('/send-contact', FormHandler),
    ('/profile-list', ProfileListHandler),
    ('/p/(.*)', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
   # ('/new-contacts', AddHomieHandler),
    ('/profile-edit', ProfileEditHandler),
    ('.*', MainHandler),
])
