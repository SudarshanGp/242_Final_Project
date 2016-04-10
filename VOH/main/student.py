from .. import open_db_connection, close_db_connection
from werkzeug.security import generate_password_hash

def add_student(username, password, name, net_id,user_type):
    """
    @author: Nihal
    Add a student to the DB
    :param username: Username
    :param password: Password
    :param name: Name
    :param net_id: Net ID
    :param user_type: Student
    :return:
    """
    # Create Student dict for table
    student = {
        "username":username,
        "password": generate_password_hash(password),
        "name": name,
        "net_id":net_id,
        "type":user_type
    }
    # Add Student value
    client, db = open_db_connection()
    db["student_table"].insert(student)
    close_db_connection(client)

def get_student(username):
    """
    @author: Nihal
    Returns Username
    :param username: Username
    :return: User
    """
    # Open Connection
    client, db = open_db_connection()
    # Find Student
    student = list(db["student_table"].find({"username":username}))
    # Close Connection
    close_db_connection(client)
    return student