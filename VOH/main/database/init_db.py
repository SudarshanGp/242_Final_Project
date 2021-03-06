from VOH import open_db_connection, close_db_connection
import datetime
import random

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
        db[table].insert({"net_id": user.replace("\r\n", "").encode("utf-8")})
    close_db_connection(client)


def add_to_online_db(table, user_list):
    """
    Creates a db table for list of online TA's
    By default, every body is offline
    :param table: table to add to
    :param user_list: List of values
    :return: None
    """
    cur_time = datetime.datetime.now()
    client, db = open_db_connection()
    db[table].remove()
    for user in user_list:
        net_id = user.replace("\r\n", "").encode("utf-8")
        db[table].insert({"net_id": net_id, "status": "offline", "_id": net_id, "total_time":random.random()*200, "last_login":cur_time})
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
        add_to_rating_db("ta_rating", user_list[1:])

def add_to_rating_db(table, user_list):
    """
    Initialize the Ratings DB
    :param table:
    :param user_list:
    :return:
    """
    client, db = open_db_connection()
    db[table].remove()
    for user in user_list:
        net_id = user.replace("\r\n", "").encode("utf-8")
        db[table].insert({"ta": net_id, "_id": net_id, "score":random.random()*5})
    close_db_connection(client)

def create_student_list(student_list):
    """
    :param student_list: Student LIST of all valid Students
    :return: None
    """
    with open(student_list, "r") as student_file:
        # Read all lines
        user_list = student_file.readlines()
        # Add Students
        add_to_db("student_list", user_list[1:])
