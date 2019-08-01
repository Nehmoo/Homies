from google.appengine.ext import ndb


class ContactProfile(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone_number = ndb.IntegerProperty()


class HomiesProfile(ndb.Model):
<<<<<<< HEAD
   name = ndb.StringProperty()
   email = ndb.StringProperty()
   last_update = ndb.DateTimeProperty(auto_now=True)
   phone_number = ndb.IntegerProperty()
   user_contacts = ndb.KeyProperty(ContactProfile,repeated=True)
=======
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    phone_number = ndb.IntegerProperty()
    user_contacts = ndb.KeyProperty(ContactProfile, repeated=True)

>>>>>>> 583e810c4b82cc346dd1e10ee7905ec2d229484f


