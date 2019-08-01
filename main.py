import webapp2
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
        socialdataapp.ensure_profile(user.email())
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
                contacts = []
                for key in profile.user_contacts:
                    contacts.append(key.get())
                values['user_contacts']= contacts
                
            else:
                profile = socialdataapp.ensure_profile(get_user_email())
                socialdataapp.create_user_profile(get_user_email())
                
        render_template(self, 'mainpageapp.html', values)

    def post(self):
        print "Entering POST for MainHandler"
        from_address = 'anything@yeetbruh.appspotmail.com'
        email = self.request.get('email')
        print "Email: " + email
        mail.send_mail(from_address, email, 'Kisses', 'Your homie has just sent you a kiss!')
        values = get_user_data()
        values['message'] = 'The kiss has been sent.'
        render_template(self, 'messagesent.html', values)
        print "Leaving POST for MainHandler"

        


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


class ListContactHandler(webapp2.RequestHandler):
    def get(self):
        email = get_user_email()
        if email:
            contacts = socialdataapp.get_contact(email)
            values = get_user_data()
            values['contacts'] = contacts
            render_template(self, 'contact-list.html', values)
        else:
            self.response.out.write('login, homie')

# class ContactSaveHandler(webapp2.RequestHandler):
#     def post(self):
#         userEmail = get_user_email()
#         if not email:
#             self.redirect('/')
#         else:
#             name = self.request.get('name')
#             phone_number = self.request.get('phone_number')
#             email = self.request.get('email')
#             values = 


class ContactSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            phone_number = self.request.get('phone_number')
            contact_email = self.request.get('email')
            values = get_user_data()
            values['name'] = name
            values['email'] = email
            values['phonenumber'] = phone_number
            if error_text:
                values['errormsg'] = error_text
            else:
                socialdataapp.save_contact(email, contact_email, name, int(phone_number)) 
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
          'email': email}

class NotFoundHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('that path is not mapped.')
    def post(self):
        self.response.out.write('that path is not mapped.')

app = webapp2.WSGIApplication([
    ('/send-contact', FormHandler),
    ('/profile-list', ProfileListHandler),
    ('/contact-list', ListContactHandler),
    ('/p/(.*)', ProfileViewHandler),
    ('/profile-save', ContactSaveHandler),
    ('/new-contacts', ListContactHandler),
    ('/profile-edit', ProfileEditHandler),
    ('/', MainHandler),
    ('.*', NotFoundHandler),
])
