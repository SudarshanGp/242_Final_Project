from VOH import open_db_connection, close_db_connection
from werkzeug.security import generate_password_hash


def check_in_student_list(net_id):
    """
    Checks if student is VALID or not
    :param net_id: Student's netID
    :return: True if netID is part of Student List
    """
    client, db = open_db_connection()
    if len(list(db["student_list"].find({"net_id": net_id}))) > 0:
        close_db_connection(client)
        return True
    close_db_connection(client)
    return False


def check_student_registration(net_id):
    """
    Checks if student has already Registered
    :param net_id: Student's netID
    :return: True if netID is registered
    """
    client, db = open_db_connection()
    if len(list(db["student_table"].find({"net_id": net_id}))) > 0:
        close_db_connection(client)
        return True
    close_db_connection(client)
    return False


def add_student(password, name, net_id, user_type):
    """
    Add a student to the DB
    :param password: Password
    :param name: Name
    :param net_id: Net ID
    :param user_type: Student
    :return: None
    """
    # Create Student dict for table
    student = {
        "password": generate_password_hash(password),
        "name": name,
        "net_id": net_id,
        "type": user_type
    }
    # Add Student value
    client, db = open_db_connection()
    db["student_table"].insert(student)
    close_db_connection(client)


def get_student(net_id):
    """
    Returns Student Details of a given net_id
    :param net_id: NetID of student
    :return: Student Details
    """
    # Open Connection
    client, db = open_db_connection()
    # Find Student
    student = list(db["student_table"].find({"net_id": net_id}))
    # Close Connection
    close_db_connection(client)
    return student
