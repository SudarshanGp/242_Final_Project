from .. import open_db_connection, close_db_connection

def add_TA(username, password, name, net_id,user_type):

    # Create TA dict for table
    ta = {
        "username":username,
        "password": password,
        "name": name,
        "net_id":net_id,
        "type":user_type
    }
    # Add TA value
    client, db = open_db_connection()
    db["ta_table"].insert(ta)
    close_db_connection(client)

def get_TA(username):
    client, db = open_db_connection()
    ta =  list(db["ta_table"].find({"username":username}))
    close_db_connection(client)
    return ta