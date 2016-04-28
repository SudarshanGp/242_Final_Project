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

@socketio.on('add_rating_to_db', namespace='/chat_session')
def add_rating_to_db(data):
    """
    leave function catches any a left signal emitted by socketIO client
    It emits a signal to all users in that room notifying that the user has left the chat conversation
    :param message: Leave Message
    """

    if TA.check_in_ta_list(data['rating_for']):
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
        else:
            db['ta_rating'].insert({"ta":data['rating_for'], '_id':data['rating_for'], 'score':int(data['rating'])})
    # Close Connection
        close_db_connection(client)
    else:
        client, db = open_db_connection()
        cur_val = list(db['student_rating'].find({"student":data['rating_for']}))
        if len(cur_val) == 1:
            db["student_rating"].update_one({
                '_id': data['rating_for']
                }, {
                '$set': {
                    'score': cur_val[0]["score"] + int(data['rating'])
                }
            }, upsert=False)
        else:
            db['student_rating'].insert({"student":data['rating_for'], '_id':data['rating_for'], 'score':int(data['rating'])})
    # Close Connection
        close_db_connection(client)



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
