from pymongo import *
from flask import Flask
from flask_socketio import *

app = Flask(__name__)
socketio = SocketIO(app)

# client = MongoClient('104.131.185.191', 27017)
# db = client["225VOH"]

from socket_test.views import api
app.register_blueprint(api)