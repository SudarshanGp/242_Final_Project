from flask import Flask
from flask_socketio import *
from pymongo import *


socketio = SocketIO()

app = Flask(__name__)

def create_app(debug=False):
    """Create an application."""
    global app
    app.config.from_object(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.debug = debug
    app.config['SECRET_KEY'] = 'asdq2312ds1242!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

def open_db_connection():
    # client = MongoClient('104.131.185.191', 27017)
    client = MongoClient()
    db = client["225VOH"]
    return client, db

def close_db_connection(client):
    client.close()