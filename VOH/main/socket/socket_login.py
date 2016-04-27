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



@socketio.on('logout_alert', namespace='/queue')
def ta_logout(data):
    """
    When a TA Logs out, every student must be alerted
    """
    alert = {"message": data["name"] + " has left 225VOH!"}
    emit('logout_alert', alert, namespace='/queue', broadcast=True)


@socketio.on('student_logout', namespace='/queue')
def student_logout(data):
    """
    When a student logs out, the student is removed from all Queues
    Updated Queues are emitted to all TA's
    """
    remove_data = {
        "student": session["net_id"],
    }
    print remove_data
    new_data = TA.remove_from_queue_db(remove_data)

    emit('student_logout', remove_data, namespace='/queue', broadcast=True)
