import os
import subprocess
from database import TA
from flask import render_template, request, redirect, url_for, jsonify
from flask_socketio import *
from database import student
from database import init_db
from VOH import socketio
import requests
from flask.ext.socketio import emit, join_room, leave_room

from VOH.main.database.authentication import *
from VOH.main.forms import RegistrationForm, LoginForm, TARating, StudentRating
from . import main
from .. import app

"""
    views.py is in charge of routing different server requests from clients.
"""



@main.route('/index/')
@main.route('/')
def main_page():
    """
    Routed to main_page() on load of website
    :return: Renders base.html
    """

    if "net_id" in session:
        return flask.redirect('/'+session['type']+'/'+str(session["net_id"]))

    return render_template("base.html", login_status = check_login_status())

@main.route('/chat/<path>/')
def chat_main(path):
    """
    Routed to /chat/<path> with the chat.html page rendered.
    Contains a chat div as well as a codeshare embed
    :return: Renders chat.html
    """
    form = ""
    if session["type"] == "TA":
        form = StudentRating()
    else:
        form = TARating()
    return render_template('chat.html', codeshare = session["link"], name = session["type"], form = form)

@main.route('/chat/<path>/<link>')
def chat(path, link):
    """
    Routed to /chat/<path>/<link>
    This is a unique function that creates a link between a TA and a Student
    Redirects to /chat/<path> to render the chat page with the codeshare link
    """

    code_link = "https://codeshare.io/"+link
    session["link"] = code_link
    return flask.redirect(url_for("main.chat_main",path=path))



@main.route('/Login/')
@main.route('/login/')
def login():
    """
    Create a login form and pass that into render_template so as to populate the form
    :return: Renders login.html
    """
    form = LoginForm()
    return render_template("login.html", form = form,login_status = check_login_status())


@main.route('/register/')
def register():
    """
    Create a registration form and pass that into render_template so as to populate the form
    :return: Renders register.html
    """
    form = RegistrationForm()
    return render_template("register.html", form = form,login_status = check_login_status())


@main.route('/register/', methods=["POST"])
def register_user():
    """
    Registers user by collecting all form data
    and validating the data
    Also updates the session variables
    :return: Renders register.html
    """

    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        if form.instructor_type.data == "TA":
            TA.add_TA(form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)
        elif form.instructor_type.data == "student":
            student.add_student(form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)

        session['net_id'] = form.net_id.data
        session['type'] = form.instructor_type.data
        session['name'] = form.name.data
        if session['type'] == 'TA':
            TA.set_ta_status(session['net_id'],"online")
        return flask.redirect('/'+session['type']+'/'+str(form.net_id.data))
    else:

        return render_template("register.html", form = form,login_status = check_login_status())


@main.route('/authenticate/', methods=["POST"])
def authenticate_login():
    """
    Authenticates Login and throws error if wrong
    """
    form = LoginForm(request.form)

    if form.validate():
        session['net_id'] = str(form.net_id.data)
        session['type'] = str(form.instructor_type.data)

        if session['type'] == 'TA':
            TA.set_ta_status(session['net_id'],"online")
            session['name'] = TA.get_TA(session['net_id'])[0]["name"]
        else:
            session['name'] = student.get_student(session['net_id'])[0]["name"]
        return flask.redirect('/'+session['type']+'/'+session['net_id'])

    return render_template('login.html', form=form,login_status = check_login_status())


@main.route('/instructor/',methods = ["GET","POST"])
def instructor_view():
    """
    Creates an instructor view with added functionality for file uploading with proper message feedback
    :return: template which returns a instructor view along with the message if file upload is successful
    """
    message = "No file uploaded"
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            path_of_file = "VOH/" + os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_of_file)
            upload_file(path_of_file)
            message = "File has been uploaded!"
        else:
            message = "No file to upload!"
    return render_template("instructor.html", message = message,login_status = check_login_status())

def upload_file(file_path):
    """
    Upload file contents to Database from Instructor View
    """
    if "TA" in open(file_path).readline():
        init_db.create_ta_list(file_path)
    elif "student" in open(file_path).readline():
        init_db.create_student_list(file_path)

@main.route('/Logout/', methods = ["GET", "POST"])
def logout():
    """
    At logout, changes sessions variables
    :return: None
    """
    if session['type'] == 'TA':
        TA.set_ta_status(session['net_id'],"offline")
    TA.clear_ta_queue(session['net_id'])
    name = session["name"]
    session.clear()
    return jsonify({"name":name})