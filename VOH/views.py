from flask import Flask, Blueprint
from flask import render_template, request
from VOH import app
from authentication import *
api = Blueprint('api', __name__)


@api.route('/login/')
def login():
    """
    Default Login Page
    :return:
    """
    return render_template("login.html")

@api.route('/register/')
def register():
    return render_template("register.html")

@api.route('/authenticate/', methods=["POST"])
def authenticate_login():
    """
    Validation of Credentials
    :return:
    """
    username = request.form["username"]
    password = request.form["password"]
    print username, password
    if authenticate_user(username, password):
        return "Success"
    return "ADfs"

@app.errorhandler(Exception)
def exception_handler(error):

    return 'ERROR ' + repr(error)