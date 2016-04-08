from flask import Flask
from flask_socketio import *
from pymongo import *


socketio = SocketIO() # Create instance of socketio app

app = Flask(__name__)


def create_app(debug=False):
    """
    @author : Sudarshan Govindprasad
    create_app creates an Flask app object, and a socket io object.
    It also registers a blue print that is imported by the files in the main package
    :param debug: debug Flag True or False
    """
    global app
    print("HERE")
    app.config.from_object(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.debug = debug
    app.config['SECRET_KEY'] = 'asdq2312ds1242!67#'
    print("CONFIGURING APP")
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print("CONFIGURING blueprint")

    socketio.init_app(app)
    print("CONFIGURING SOCKETIO")
    return app


def open_db_connection():
    """
    Creates mongodb connection and returns client and current database instance
    """
    client = MongoClient('104.131.185.191', 27017)
    # client = MongoClient()
    db = client["225VOH"]
    return client, db


def close_db_connection(client):
    """
    Closes mongo db connection
    """
    client.close()