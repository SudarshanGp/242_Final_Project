from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect, Flask, url_for
from flask_socketio import *
from flask.ext.socketio import emit, join_room, leave_room
from VOH import open_db_connection, close_db_connection
import datetime
import time
from VOH import socketio
from VOH.main.database import TA
import os, subprocess

@socketio.on('join', namespace='/chat_session')
def join(message):
    """
    join function catches any a join signal emitted by socketIO client
    adds client to a particular room identified by the message passed in from the socket client.
    Join Message returned is broadcasted to everyone in that specific room
    :param message: Join Message
    """

    join_room(str(message['room']))
    session['room'] = str(message['room'])
    emit('status', {'msg': session['net_id'] + ' is now in the conversation'}, namespace='/chat_session',
         room=str(message['room']))  # Emits signal to a particular chat conversation


@socketio.on('text', namespace='/chat_session')
def converse(message):
    """
    converse function catches any a text signal emitted by socketIO client
    It emits a signal to all users in that room to add that message to the chat box
    :param message: Conversation Message
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    client, db = open_db_connection()
    db['chat_log'][session['room']].insert(
        dict(room=session['room'].encode("utf-8"), message=message, by = session.get('net_id'), time=st.encode("utf-8")))
    close_db_connection(client)

    emit('message', {'msg': session.get('net_id') + ':' + message['msg']}, room=session['room'])


@socketio.on('editor_change', namespace='/chat_session')
def editor(message):
    print(message, "EDITOR")
    emit('editor_change_api',
         {'message': message['change'], 'all_data': message['all_data'], 'my_id': message['my_id']},
         room=session['room'])


@socketio.on('left', namespace='/chat_session')
def leave(message):
    """
    leave function catches any a left signal emitted by socketIO client
    It emits a signal to all users in that room notifying that the user has left the chat conversation
    :param message: Leave Message
    """
    chatID = session.get('room')
    leave_room(chatID)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    client, db = open_db_connection()
    db['chat_log'][session['room']].insert(
        dict(room=session['room'].encode("utf-8"), message=session.get('net_id') + ' has now left the conversation.', by = session.get('net_id'), time=st.encode("utf-8")))
    close_db_connection(client)
    emit('status', {'msg': session.get('net_id') + ' has now left the conversation.'}, room=session['room'])


@socketio.on('loginTA', namespace='/queue')
def add_ta_online(data):
    """
    Socket End point for a TA who is online
    Updates the TA's status to online and updates all pages as well
    :param data: Data passed in by socketio client
    :return: None
    """
    online_ta = TA.get_online_ta()
    ret_list = {}
    for index in range(len(online_ta)):
        ta = online_ta[index]
        ta.pop('_id', None)
        ret_list[index] = (ta)
    new_data = TA.get_ta_queue(session.get('net_id'))

    emit('online', {"online": ret_list, "queue": new_data}, namespace='/queue', broadcast=True)


@socketio.on('add_student', namespace='/queue')
def add_student(data):
    """
    Listener for when a student clicks on Joining a TA's queue and broadcasts queue to all TAs
    :param data: Data passed in by socketio client
    :return: None
    """
    ret_data = {
        "student": session["net_id"],
        "ta": data["net_id"]
    }
    print "Adding Student to Queue Socket"
    new_data = TA.add_to_queue_db(ret_data)
    emit('add_student_queue', {"queue": new_data}, namespace='/queue', broadcast=True)


@socketio.on('remove_student', namespace='/queue')
def remove_student(data):
    """
    Listener for when a student clicks on Joining a TA's queue and broadcasts queue to all TAs
    :param data: Data passed in by socketio client
    :return: None
    """
    remove_data = {
        "student": session["net_id"],
        "ta": data["net_id"]
    }
    print remove_data
    new_data = TA.remove_from_queue_db(remove_data)
    print new_data
    emit('add_student_queue', {"queue": new_data}, namespace='/queue', broadcast=True)


@socketio.on('remove_student_answer', namespace='/queue')
def remove_student(data):
    """
    Listener for when a TA clicks on Answer on the TA's queue and removes the student
    from the TA's queue by removing the student from the queue database
    :param data: Data passed in by socketio client
    :return: None
    """
    remove_data = {
        "student": data["net_id"],
        "ta": session["net_id"]
    }
    print remove_data
    new_data = TA.remove_from_queue_db(remove_data)
    print new_data


@socketio.on('answer_student', namespace='/queue')
def answer_student(data):
    """
    Needs to make a socket call to shift student and TA to a specific room. There will be an another function which
    catches a signal that is emitted back (Python code will add both users to a room on this signal) and will return
    a href to redirect the users {unique roomID} and will be redirected using window's href in the javascript code
    :param data: data from socketio call
    """

    join_room(data['ta']) # Joined ta's room
    new_data = {'room' : data['net_id'], 'student': data['net_id'], 'ta': data['ta']}

    path = os.path.abspath("VOH/codeshare.py")
    print path

    link = subprocess.check_output(["python", path])

    # emit('answer_info', new_data, namespace='/queue', broadcast=True)

    # Adding a new collection for particular student, ta pair. Collection name is the ta's netID
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    client, db = open_db_connection()
    db['chat_log'][data['ta']].insert(
        dict(room=data['ta'].encode("utf-8"), message="Started Conversation", time=st.encode("utf-8")))
    close_db_connection(client)
    emit('student_join_emit', {"student" : data['net_id'], "ta" : data['ta'], "link":link}, broadcast = True )



@socketio.on('student_join', namespace='/queue')
def student_room_success(data):
    """
    When a Student joins the TA's room, they are both in the same room and its time to start the chat.
    A start_chat signal is emitted to a particular room in the namespace asking both clients in to
    redirect to the chat page
    :param data: Data about room
    """
    join_room(data['ta'])
    json_data = {'room' : data['ta'], "link":data["link"]}
    emit('start_chat', json_data , namespace = '/queue', room = data['ta'], broadcast = True)


@socketio.on('logout_alert', namespace='/queue')
def ta_logout(data):
    alert = {"message": data["name"] + " has left 225VOH!"}
    emit('logout_alert', alert, namespace='/queue', broadcast=True)


@socketio.on('student_logout', namespace='/queue')
def ta_logout(data):
    remove_data = {
        "student": session["net_id"],
    }
    print remove_data
    new_data = TA.remove_from_queue_db(remove_data)

    emit('student_logout', remove_data, namespace='/queue', broadcast=True)


@socketio.on('join', namespace='/queue')
def join(data):
    """
    Function is called when a TA and Student need to join a particular room so that they can be
    directed to a unique URL to start their chat
    :param data: Data Containing information about the room
    """
    join_room(data['id'])
    emit('join_room_ta', {'msg': "hi, you are in room " + data['id']},
         room=data['id'])  # Emits signal to a particular chat conversation
