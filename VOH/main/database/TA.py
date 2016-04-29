from VOH import open_db_connection, close_db_connection
from werkzeug.security import generate_password_hash
import datetime

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
    print "Adding Student to Queue TA.py"
    if len(list(table.find(ret_data))) == 0:
        table.insert_one(ret_data)
    close_db_connection(client)
    return get_ta_queue(ret_data["ta"])

def remove_from_queue_db(remove_data):
    client, db = open_db_connection()
    table = db["ta_queue"]
    table.remove(remove_data)
    close_db_connection(client)
    if "ta" in remove_data:
        return get_ta_queue(remove_data["ta"])
    return None

def get_ta_queue(net_id):
    """
    Returns the TA queue table
    :return: Returns all TA Queue
    """
    client, db = open_db_connection()
    new_data = list(db["ta_queue"].find())
    for key, value in enumerate(new_data):
        del value['_id']
    close_db_connection(client)
    print "Returning a List of Queue for TA"
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
        net_id_list[index].pop("last_login",None)


def get_online_ta():
    """
    Returns a list of all Online TA
    :return: A list of online TA's
    """
    # Open Connection
    client, db = open_db_connection()

    ta_list = list(db["online_ta"].find({"status": "online"}))
    update_ta_list(ta_list)
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

def clear_ta_queue(net_id):
    """
    Clears TA queue at Logout
    """
    client, db = open_db_connection()
    table = db["ta_queue"]
    table.remove({"ta":net_id})
    close_db_connection(client)

def set_ta_status(net_id, status):
    """
    Sets the status of the given TA to online/offline
    :param net_id: net_ID of TA
    :param net_id: Status of TA
    :return: None
    """
    # Logs the current time and updates the total time of a TA on LOGOUT
    cur_time = datetime.datetime.now()
    client, db = open_db_connection()
    if status == "online":
        # Logs Current Login time
        db["online_ta"].update_one({
            '_id': net_id
        }, {
            '$set': {
                'status': status,
                'last_login':cur_time
            }
        }, upsert=False)
    else:
        ta_data = list(db["online_ta"].find({"_id":net_id}))
        # Updates total time
        total_time = ta_data[0]["total_time"] + (cur_time - ta_data[0]["last_login"]).seconds
        db["online_ta"].update_one({
            '_id': net_id
        }, {
            '$set': {
                'status': status,
                'total_time':total_time
            }
        }, upsert=False)

    # Close Connection
    close_db_connection(client)

def get_ta_ratings():
    """
    Returns a list of TA ratings
    :return:
    """
    ta_ratings = []
    client, db = open_db_connection()
    ta_list = list(db["ta_rating"].find({}))
    for ta in ta_list:
        ta_ratings.append({
            "name":ta["ta"],
            "score":ta["score"]
        })

    close_db_connection(client)

    return ta_ratings

def get_ta_timings():
    """
    Returns a list of TA timings Logged into the DB
    :return:
    """
    ta_timings = []
    client, db = open_db_connection()
    ta_list = list(db["online_ta"].find({}))
    for ta in ta_list:
        ta_timings.append({
            "name":ta["_id"],
            "time in minutes":ta["total_time"]/60
        })

    close_db_connection(client)
    return ta_timings

def add_ta_rating(data):
    client, db = open_db_connection()
    cur_val = list(db['ta_rating'].find({"ta":data['rating_for']}))
    if len(cur_val) == 1:
        db["ta_rating"].update_one({
            '_id': data['rating_for']
            }, {
            '$set': {
                'score': cur_val[0]["score"] + int(data['rating'])
            }
        }, upsert=False)
    close_db_connection(client)