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
    return render_template("login.html")


@app.route('/login', methods=["POST"])
def authenticate_login():
    """
    Validation of Credentials
    :return:
    """
    username = request.form["username"]
    password = request.form["password"]
    if authenticate_user(username, password):
        return render_template("success.html")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)