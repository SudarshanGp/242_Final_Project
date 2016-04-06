from flask import Flask
from flask_socketio import *
from pymongo import *


socketio = SocketIO()
client = MongoClient('104.131.185.191', 27017)
db = client["225VOH"]

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.debug = debug
    app.config['SECRET_KEY'] = 'asdq2312ds1242!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

