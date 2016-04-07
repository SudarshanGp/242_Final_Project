from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect
from flask_socketio import *

from VOH.main.forms import RegistrationForm, LoginForm
from authentication import *
from . import main
from .. import app
import os


@main.route('/')
@main.route('/index/')
def main_page():
    return render_template("base.html")


@main.route('/login/')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)


@main.route('/register/')
def register():
    form = RegistrationForm()
    return render_template("register.html", form = form)

@main.route('/register/', methods=["POST"])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        print form.username.data, form.password.data
    return "Success"

@main.route('/authenticate/', methods=["POST"])
def authenticate_login():
    print("in authenticate")
    form = LoginForm(request.form)
    if authenticate_user(form.username, form.password):
        return jsonify(response = "Success")
    return jsonify(response = 'ADfs')


@main.route('/instructor/',methods = ["GET","POST"])
def instructor_view():
    message = "No file uploaded"
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            path_of_file = "VOH/" + os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_of_file)
            message = "File has been uploaded!"
        else:
            message = "No file to upload!"
    return render_template("instructor.html", message = message)

