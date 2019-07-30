from socialmodelapp import HomiesProfile

def save_profile(email, name, phone_number):
    p = get_user_profile(email)
    if p:
        p.name = name
        p.phone_number = phone_number
    else:
        p = HomiesProfile(email=email, name=name, phone_number=int(phone_number))
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
    return None

def get_recent_profiles():
    q = HomiesProfile.query().order(-HomiesProfile.last_update)
    return q.fetch(50)

