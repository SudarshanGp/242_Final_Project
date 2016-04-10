from .. import open_db_connection, close_db_connection
from werkzeug.security import generate_password_hash

def check_in_ta_list(net_id, db):
    if len( list(db["ta_list"].find({"net_id":net_id})))> 0:
        return True
    return False

def add_TA(password, name, net_id,user_type):
    """
    @author: Nihal,Aadhya
    :param username: Username
    :param password: Password
    :param name: name
    :param net_id: Net Id
    :param user_type: TA
    :return:
    """
    # Create TA dict for table
    ta = {
        "password": generate_password_hash(password=password),
        "name": name,
        "net_id":net_id,
        "type":user_type
    }
    # Add TA value
    client, db = open_db_connection()
    if check_in_ta_list(net_id, db):
        db["ta_table"].insert(ta)
    close_db_connection(client)

def get_TA(net_id):
    """
    Return TA with username
    :param username: username
    :return:
    """
    # Open Connection
    client, db = open_db_connection()
    # Find
    ta =  list(db["ta_table"].find({"net_id":net_id}))
    # Close Connection
    close_db_connection(client)
    return ta