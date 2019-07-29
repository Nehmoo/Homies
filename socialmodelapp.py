from google.appengine.ext import ndb

class HomiesProfile(ndb.Model):
    nickame = ndb.StringProperty()
    email = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    phone_number = ndb.IntegerProperty()
    