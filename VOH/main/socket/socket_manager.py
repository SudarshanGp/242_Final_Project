from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect
from flask_socketio import *
from flask.ext.socketio import emit, join_room, leave_room
from VOH import open_db_connection, close_db_connection
from VOH import socketio
from VOH.main.database import TA


@socketio.on('join', namespace='/chat')
def join(message):
    """
    join function catches any a join signal emitted by socketIO client
    adds client to a particular room identified by chatID.
    Join Message returned is broadcasted to everyone in that specific room
    :param message: Join Message
    """

    chatID = session.get('chatID')  # Retrieve chatID from session i
    join_room(chatID)  # Join chatID room
    emit('status', {'msg': session.get('netID') + ' is now in the conversation'},
         room=chatID)  # Emits signal to a particular chat conversation


@socketio.on('text', namespace='/chat')
def converse(message):
    """
    converse function catches any a text signal emitted by socketIO client
    It emits a signal to all users in that room to add that message to the chat box
    :param message: Conversation Message
    """
    chatID = session.get('chatID')
    emit('message', {'msg': session.get('netID') + ':' + message['msg']}, room=chatID)


@socketio.on('left', namespace='/chat')
def leave(message):
    """
    leave function catches any a left signal emitted by socketIO client
    It emits a signal to all users in that room notifying that the user has left the chat conversation
    :param message: Leave Message
    """
    chatID = session.get('chatID')
    leave_room(chatID)
    emit('status', {'msg': session.get('netID') + ' has now left the conversation.'}, room=chatID)


@socketio.on('loginTA', namespace='/login')
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
    new_data = TA.get_ta_queue()

    emit('online', {"online": ret_list, "queue": new_data}, namespace='/login', broadcast=True)


@socketio.on('add_student', namespace='/login')
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
    new_data = TA.add_to_queue_db(ret_data)

    print(new_data, "new DATA")
    emit('add_student_queue', new_data, namespace='/login', broadcast=True)
