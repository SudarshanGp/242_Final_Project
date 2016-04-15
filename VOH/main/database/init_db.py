from VOH import open_db_connection, close_db_connection


def add_to_db(table, user_list):
    """
    Add values to DB
    :param table: table to add to
    :param user_list: List of values
    :return: None
    """

    client, db = open_db_connection()
    db[table].remove()
    for user in user_list:
        db[table].insert({"net_id":user.replace("\r\n","").encode("utf-8")})
    close_db_connection(client)


def add_to_online_db(table, user_list):
    """
    Creates a db table for list of online TA's
    By default, every body is offline

    :return:
    """
    client, db = open_db_connection()
    db[table].remove()
    for user in user_list:
        net_id = user.replace("\r\n","").encode("utf-8")
        db[table].insert({"net_id":net_id, "status":"offline", "_id":net_id})
    close_db_connection(client)

def create_ta_list(ta_list):
    """
    Creates TA_lIST of all Valid TA's
    :param ta_list: File
    :return: None
    """
    with open(ta_list, "r") as ta_file:
        user_list = ta_file.readlines()
        add_to_db("ta_list", user_list[1:])
        add_to_online_db("online_ta", user_list[1:])


def create_student_list(student_list):
    """
    :param student_list: Student LIST of all valid Students
    :return: None
    """
    with open(student_list, "r") as student_file:
        # Read all lines
        user_list = student_file.readlines()
        # Add Students
        add_to_db("student_list", user_list)
