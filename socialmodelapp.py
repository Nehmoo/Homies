from google.appengine.ext import ndb

class HomiesProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    phone_number = ndb.IntegerProperty()
    user_contacts = ndb.StringProperty()
    