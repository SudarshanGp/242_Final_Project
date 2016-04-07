from .. import db

def add_to_db(table, user_list):
    for user in user_list:
        table.insert({"netid":user.encode("utf-8")})

def create_ta_list(ta_list):

    with open(ta_list, "r") as ta_file:
        user_list = ta_file.readlines()
        add_to_db(db["ta_list"], user_list)

def create_student_list(student_list):

    with open(student_list, "r") as student_file:
        user_list = student_file.readlines()
        add_to_db(db["student_list"], user_list)
