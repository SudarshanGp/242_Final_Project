from .. import open_db_connection, close_db_connection

def add_TA(username, password, name, net_id,user_type):
    """
    @author: Nihal
    :param username: Username
    :param password: Password
    :param name: name
    :param net_id: Net Id
    :param user_type: TA
    :return:
    """
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
    """
    Return TA with username
    :param username: username
    :return:
    """
    # Open Connection
    client, db = open_db_connection()
    # Find
    ta =  list(db["ta_table"].find({"username":username}))
    # Close Connection
    close_db_connection(client)
    return ta