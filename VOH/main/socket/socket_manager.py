from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect
from flask_socketio import *
from flask.ext.socketio import emit, join_room, leave_room

from VOH import socketio


@socketio.on('join', namespace='/chat')
def join(message):
    """
    @author : Sudarshan
    join function catches any a join signal emitted by socketIO client
    adds client to a particular room identified by chatID.
    Join Message returned is broadcasted to everyone in that specific room
    :param message: Join Message
    """

    chatID = session.get('chatID') # Retrieve chatID from session i
    join_room(chatID) # Join chatID room
    emit('status', {'msg': session.get('netID') + ' is now in the conversation'}, room=chatID)  #Emits signal to a particular chat conversation


@socketio.on('text', namespace='/chat')
def converse(message):
    """
    @author : Sudarshan
    converse function catches any a text signal emitted by socketIO client
    It emits a signal to all users in that room to add that message to the chat box
    :param message: Conversation Message
    """
    chatID = session.get('chatID')
    emit('message', {'msg': session.get('netID') + ':' + message['msg']}, room=chatID)


@socketio.on('left', namespace='/chat')
def leave(message):
    """
    @author : Sudarshan
    leave function catches any a left signal emitted by socketIO client
    It emits a signal to all users in that room notifying that the user has left the chat conversation
    :param message: Leave Message
    """
    chatID = session.get('chatID')
    leave_room(chatID)
    emit('status', {'msg': session.get('netID') + ' has now left the conversation.'}, room=chatID)

