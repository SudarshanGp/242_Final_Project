from pymongo import *
from flask import Flask

app = Flask(__name__)
client = MongoClient()
db = client["225VOH"]