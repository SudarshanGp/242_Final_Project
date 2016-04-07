from .. import db


def get_user_db(user_type):
    """
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


def authenticate_user(username, password, user_type):
    """
    Validates User Credentials
    :param username: Username
    :param password: Password
    :return:
    """

    # Gets the users table
    users_table = get_user_db(user_type)

    # Get's user with this username
    user = list(users_table.find({"username":username}))

    # If ONE user exists
    if len(user) == 1:
        # If password matches
        if user[0]["password"] == password:
            return True
        else:
            return False
    # No one valid was found
    return False