from .. import open_db_connection, close_db_connection


def add_to_db(table, user_list):
    """
    @author: Nihal
    Add values to DB
    :param table: table to add to
    :param user_list: List of values
    :return: None
    """

    # Open Connection
    client, db = open_db_connection()
    # Clear Table
    db[table].remove()
    # Insert all Students / TA's
    for user in user_list:
        db[table].insert({"netid":user.replace("\r\n","").encode("utf-8")})
    # Close Connection
    close_db_connection(client)


def create_ta_list(ta_list):
    """
    @author: Nihal
    Creates TA_lIST of all Valid TA's
    :param ta_list: File
    :return: None
    """
    with open(ta_list, "r") as ta_file:
        # Read all lines into a list
        user_list = ta_file.readlines()
        # Add TA's
        add_to_db("ta_list", user_list)


def create_student_list(student_list):
    """
    @author: Nihal
    :param student_list: Student LIST of all valid Students
    :return: None
    """
    with open(student_list, "r") as student_file:
        # Read all lines
        user_list = student_file.readlines()
        # Add Students
        add_to_db("student_list", user_list)
