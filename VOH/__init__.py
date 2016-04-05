from pymongo import *
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
client = MongoClient('104.131.185.191', 27017)
db = client["225VOH"]

from VOH.views import api
app.register_blueprint(api)