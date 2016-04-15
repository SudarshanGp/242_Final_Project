from VOH import open_db_connection, close_db_connection
from werkzeug.security import check_password_hash
from flask import session


def get_user_db(user_type, db):
    """
    Gets USERS Table
    :return: Returns a list of users of user_type from database
    """
    users_table = None

    if user_type == "TA":
        users_table = db["ta_table"]
    elif user_type == "student":
        users_table = db["student_table"]

    return users_table


def authenticate_user(net_id, password, user_type):
    """
    Validates User Credentials
    Update: Hashing of passwords
    :param net_id: Username
    :param password: Password
    :param user_type: Type of User (TA or Student)
    :return: True or False depending on if user passes authentication check
    """
    client, db = open_db_connection()
    users_table = get_user_db(user_type, db)

    user = list(users_table.find({"net_id":net_id}))

    if len(user) == 1:
        if  check_password_hash(user[0]["password"], password):
            return True
        else:
            return False
    close_db_connection(client)
    return False


def check_login_status():
    """
    Checks Login status
    :return: True if User is logged in
    """
    login_status = 'Login'
    if 'net_id' in session:
        login_status = 'Logout'
    return login_status