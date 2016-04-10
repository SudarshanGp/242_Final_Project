from .. import open_db_connection, close_db_connection
from werkzeug.security import check_password_hash

def get_user_db(user_type, db):
    """
    @author: Nihal
    Gets USERS Table
    :return:
    """
    users_table = None

    # Return TA Table
    if user_type == "TA":
        users_table = db["ta_table"]
    # Return Student Table
    elif user_type == "student":
        users_table = db["student_table"]

    return users_table


def authenticate_user(net_id, password, user_type):
    """
    @author: Nihal
    Validates User Credentials
    :param username: Username
    :param password: Password
    :return:
    """
    client, db = open_db_connection()
    # Gets the users table
    users_table = get_user_db(user_type, db)

    # Get's user with this username
    user = list(users_table.find({"net_id":net_id}))

    # If ONE user exists
    if len(user) == 1:
        # If password matches
        if  check_password_hash(user[0]["password"], password):
            return True
        else:
            return False
    # No one valid was found
    close_db_connection(client)
    return False