from socialmodelapp import HomiesProfile
from socialmodelapp import ContactProfile


def ensure_profile(email):
    if not get_user_profile(email):
        p = HomiesProfile(email = email, name = email, phone_number=0)
        p.put()


def save_profile(email):
    p = get_user_profile(email)
    if p:
        p.email = email
    else:
        p = HomiesProfile(email=email)
    p.put()


def save_contact(user_email, contact_email, contact_name, contact_number):
    p = get_user_profile(user_email) #Checks if the user is in 
    if p:
        c = ContactProfile(email = contact_email, name = contact_name, phone_number = int(contact_number))
        p.user_contacts.append(c.put())
        p.put()


def get_user_profile(email):
    q = HomiesProfile.query(HomiesProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_profile_by_name(name):
    q = HomiesProfile.query(HomiesProfile.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None #ask why this is returning nothing

def get_contact(name):
    c = ContactProfile.query(ContactProfile.name == name).fetch(1)
    for contact in c:
        return contact
    print "enter get_contacts"
    print "name: " + name
    q = HomiesProfile.query(HomiesProfile.name == name) #ask what this means
    results = q.fetch(1) #ask what q.fetch means
    profile = None
    for p in results:
       profile = p
    
    contacts = []
    for c in profile.user_contacts:
        contacts.append(c.get())
    #  ContactProfile.query(ContactProfile.id == contacts[0])
    #  temp = q.fetch(1)
    #  print temp
    # return [temp]
    # return [q.fetch(1)]
    # print "exit get_contacts"
    return contacts


def get_recent_profiles():
    q = HomiesProfile.query().order(-HomiesProfile.last_update)
    return q.fetch(50)
