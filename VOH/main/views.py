from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect
from VOH import app
from flask_socketio import *
from authentication import *
import os
api = Blueprint('api', __name__)
socketio = SocketIO(app)
thread = None # keeping track of thread
app.config['UPLOAD_FOLDER'] = 'uploads'


@api.route('/')
@api.route('/index/')
def main_page():
    return render_template("base.html")


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
        return jsonify(response = "Success")
    return jsonify(response = 'ADfs')


@api.route('/instructor/',methods = ["GET","POST"])
def instructor_view():
    message = "No file uploaded"
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            path_of_file = "VOH/" + os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print path_of_file
            file.save(path_of_file)
            message = "File has been uploaded!"
        else:
            message = "No file to upload!"
    return render_template("instructor.html", message = message)

@app.errorhandler(Exception)
def exception_handler(error):

    return 'ERROR ' + repr(error)