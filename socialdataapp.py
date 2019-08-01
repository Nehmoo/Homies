from socialmodelapp import HomiesProfile
from socialmodelapp import ContactProfile

def save_profile(email):
    p = get_user_profile(email)
    if not p:
        p = HomiesProfile(email=email)
    p.put()

def save_contact(user_email, contact_email, contact_name, contact_number):
    p = get_user_profile(user_email) 
    c = ContactProfile(email = contact_email, name = contact_name, phone_number = int(contact_number))
    p.user_contacts.append(c.put())


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
    return None

def get_recent_profiles():
    q = HomiesProfile.query().order(-HomiesProfile.last_update)
    return q.fetch(50)

