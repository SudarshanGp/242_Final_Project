from VOH import open_db_connection, close_db_connection
from werkzeug.security import generate_password_hash


def check_in_ta_list(net_id):
    """
    Checks if TA is a valid TA
    :param net_id: net_id of TA
    :return: True if net_id is TA's net_id
    """
    client, db = open_db_connection()
    if len(list(db["ta_list"].find({"net_id": net_id}))) > 0:
        close_db_connection(client)
        return True
    close_db_connection(client)
    return False


def check_ta_registration(net_id):
    """
    Checks if TA has already been registered
    :param net_id: net_id of TA
    :return: True TA is registered
    """
    client, db = open_db_connection()
    if len(list(db["ta_table"].find({"net_id": net_id}))) > 0:
        close_db_connection(client)
        return True
    close_db_connection(client)
    return False


def add_to_queue_db(ret_data):
    """
    Add's student to the Queue Table with the corresponding TA requested
    :param ret_data: Data of Queue Item
    :return: Returns Updated queue status for that TA
    """
    client, db = open_db_connection()
    table = db["ta_queue"]
    table.insert_one(ret_data)
    new_data = list(db["ta_queue"].find({}))
    for key, value in enumerate(new_data):
        del value['_id']
    close_db_connection(client)
    return new_data


def get_ta_queue():
    """
    Returns the TA queue table
    :return: Returns all TA Queue
    """
    client, db = open_db_connection()
    new_data = list(db["ta_queue"].find({}))
    for key, value in enumerate(new_data):
        del value['_id']
    close_db_connection(client)
    return new_data


def add_TA(password, name, net_id, user_type):
    """
    Adds TA to table
    :param password: Password
    :param name: name
    :param net_id: Net Id
    :param user_type: TA
    :return: None
    """
    # Create TA dict for table
    ta = {
        "password": generate_password_hash(password=password),
        "name": name,
        "net_id": net_id,
        "type": user_type
    }
    # Add TA value
    client, db = open_db_connection()
    db["ta_table"].insert(ta)
    close_db_connection(client)


def update_ta_list(net_id_list):
    """
    :param net_id_list: List of Net Id's
    :return: Update the list with Names as well
    """
    for index in range(len(net_id_list)):
        net_id = net_id_list[index]["net_id"]
        name = get_TA(net_id)[0]["name"]
        net_id_list[index]["name"] = name


def get_online_ta():
    """
    Returns a list of all Online TA
    :return: A list of online TA's
    """
    # Open Connection
    client, db = open_db_connection()

    ta_list = list(db["online_ta"].find({"status": "online"}))
    update_ta_list(ta_list)
    print ta_list
    # Close Connection
    close_db_connection(client)
    return ta_list


def get_TA(net_id):
    """
    Return TA with username
    :param net_id: net_ID of TA
    :return: Returns TA information
    """
    # Open Connection
    client, db = open_db_connection()
    # Find
    ta = list(db["ta_table"].find({"net_id": net_id}))
    # Close Connection
    close_db_connection(client)
    return ta


def set_ta_status(net_id, status):
    """
    Sets the status of the given TA to online/offline
    :param net_id: net_ID of TA
    :param net_id: Status of TA
    :return: None
    """
    client, db = open_db_connection()
    db["online_ta"].update_one({
        '_id': net_id
    }, {
        '$set': {
            'status': status
        }
    }, upsert=False)
    # Close Connection
    close_db_connection(client)
