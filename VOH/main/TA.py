from .. import db
def add_TA(username, password, name, email,user_type):

    # Create TA dict for table
    ta = {
        "username":username,
        "password": password,
        "name": name,
        "email":email,
        "type":user_type
    }
    # Add TA value
    db["ta_table"].insert(ta)

def get_TA(username):
    return list(db["ta_table"].find({"username":username}))