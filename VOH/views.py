from flask import Flask
from flask import render_template, request
from VOH import app
from authentication import *


@app.route('/login')
def login():
    """
    Default Login Page
    :return:
    """
    render_template("login.html")


@app.route('/login', methods=["POST"])
def authenticate_login():
    """
    Validation of Credentials
    :return:
    """
    username = request.form["username"]
    password = request.form["password"]
    if authenticate_user(username, password):
        render_template("success.html")
    render_template("login.html")