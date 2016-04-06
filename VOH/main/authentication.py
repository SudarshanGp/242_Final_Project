from .. import db

def get_user_db():
    """
    Gets USERS Table
    :return:
    """
    users_table = db["users"]
    return users_table

def authenticate_user(username, password):
    """
    Validates User Credentials
    :param username: Username
    :param password: Password
    :return:
    """

    # Gets the users table
    users_table = get_user_db()

    # Get's user with this username
    user = list(users_table.find({"username":username}))

    # If ONE user exists
    if len(user) == 1:
        # If password matches
        if user[0]["password"] == password:
            return True
        else:
            return False
    # No one found
    return False