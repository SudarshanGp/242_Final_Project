from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect
from flask_socketio import *
from flask.ext.socketio import emit, join_room, leave_room

from .. import socketio

print("here")

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print("ON JOINED")
    print(session)
    room = session.get('chatID')
    join_room(room)
    emit('status', {'msg': session.get('netID') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def add(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    print(" IN  GOT TEXT MESSAGE")
    room = session.get('chatID')
    emit('message', {'msg': session.get('netID') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    print("ON LEFT")
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('chatID')
    leave_room(room)
    emit('status', {'msg': session.get('netID') + ' has left the room.'}, room=room)

