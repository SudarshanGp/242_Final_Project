from .. import open_db_connection, close_db_connection

def add_student(username, password, name, email,user_type):

    # Create Student dict for table
    student = {
        "username":username,
        "password": password,
        "name": name,
        "email":email,
        "type":user_type
    }
    # Add Student value
    client, db = open_db_connection()
    db["student_table"].insert(student)
    close_db_connection(client)

def get_student(username):

    client, db = open_db_connection()
    student = list(db["student_table"].find({"username":username}))
    close_db_connection(client)
    return student