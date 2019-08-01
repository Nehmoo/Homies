from google.appengine.ext import ndb


class ContactProfile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone_number = ndb.IntegerProperty()

    
class HomiesProfile(ndb.Model):
   # name = ndb.StringProperty()
    email = ndb.StringProperty()
   # last_update = ndb.DateTimeProperty(auto_now=True)
   # phone_number = ndb.IntegerProperty()
    user_contacts = ndb.KeyProperty(ContactProfile,repeated=True)


    