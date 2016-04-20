from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect, Flask, url_for
from flask_socketio import *
from flask.ext.socketio import emit, join_room, leave_room
from VOH import open_db_connection, close_db_connection
from VOH import socketio
from VOH.main.database import TA


@socketio.on('join', namespace = '/test')
def join(message):
    """
    join function catches any a join signal emitted by socketIO client
    adds client to a particular room identified by chatID.
    Join Message returned is broadcasted to everyone in that specific room
    :param message: Join Message
    """

    join_room(str(message['room']))
    session['room'] = str(message['room'])
    emit('status', {'msg': session['net_id'] + ' is now in the conversation'}, namespace = '/test', room = str(message['room']))  # Emits signal to a particular chat conversation


@socketio.on('text',  namespace = '/test')
def converse(message, namespace = '/test'):
    """
    converse function catches any a text signal emitted by socketIO client
    It emits a signal to all users in that room to add that message to the chat box
    :param message: Conversation Message
    """
    print(message, "CONVERSE")
    emit('message', {'msg': session.get('net_id') + ':' + message['msg']}, room = session['room'])


@socketio.on('left', namespace='/test')
def leave(message):
    """
    leave function catches any a left signal emitted by socketIO client
    It emits a signal to all users in that room notifying that the user has left the chat conversation
    :param message: Leave Message
    """
    chatID = session.get('room')
    leave_room(chatID)
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
    emit('student_join_emit', {"student" : data['net_id'], "ta" : data['ta']}, broadcast = True )
    # emit('answer_info', new_data, namespace='/queue', broadcast=True)

@socketio.on('student_join', namespace='/queue')
def student_room_success(data):
    join_room(data['ta'])
    json_data = {'room' : data['ta']}
    emit('start_chat', json_data , namespace = '/queue', room = data['ta'], broadcast = True)
    print("TRYING TO REDIRECT")
    # redirect(url_for('main.chat',messages = data['ta'] ))




@socketio.on('join_room', namespace='/queue')
def join_user_room(data):
    join_room(data['room'])


@socketio.on('join', namespace='/queue')
def join(data):
    """

    """
    join_room(data['id'])  # Join chatID room
    emit('join_room_ta', {'msg':"hi, you are in room " + data['id']},
         room=data['id'])  # Emits signal to a particular chat conversation


