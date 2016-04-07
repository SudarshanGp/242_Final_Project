from .. import db

def add_student(username, password, name, email,user_type):

    # Create Student dict for table
    student = {
        "username":username,
        "password": password,
        "name": name,
        "email":email,
        "type":user_type
    }
    # Add TA value
    db["student_table"].insert(student)

def get_student(username):
    return list(db["student_table"].find({"username":username}))