from .. import open_db_connection, close_db_connection

def add_to_db(table, user_list):
    client, db = open_db_connection()
    for user in user_list:
        db[table].insert({"netid":user.encode("utf-8")})
    close_db_connection(client)

def create_ta_list(ta_list):

    with open(ta_list, "r") as ta_file:
        user_list = ta_file.readlines()
        add_to_db("ta_list", user_list)

def create_student_list(student_list):

    with open(student_list, "r") as student_file:
        user_list = student_file.readlines()
        add_to_db("student_list", user_list)
