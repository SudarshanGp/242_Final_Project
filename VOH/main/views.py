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
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':RC4-SHA'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

from VOH.main.database.authentication import *
from VOH.main.forms import RegistrationForm, LoginForm
from . import main
from .. import app

"""
    views.py is in charge of routing different server requests from clients.
"""


@main.route('/')
@main.route('/index/')
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
    Routed to /chat/<path> with the chat.html page rendered. This is routed by the socketio javascript clinet code
    when a custom chat session is created
    :return: Renders chat.html
    """
    codeshare = ""
    return render_template('chat.html', codeshare = session["link"])

@main.route('/chat/<path>/<link>')
def chat(path, link):
    """
    Routed to /chat/<path> with the chat.html page rendered. This is routed by the socketio javascript clinet code
    when a custom chat session is created
    :return: Renders chat.html
    """
    print(path)
    # netID = session.get('netID', '')
    # chatID = session.get('chatID', '')
    # if netID == '' or chatID == '':
    #     return redirect(url_for('.landing'))

    code_link = "https://codeshare.io/"+link
    # # ret = subprocess.check_output(['python', "codeshare.py"])
    # print os.path.exists("codeshare.py")
    # path = "/Users/Nihal/Desktop/codeshare.py"
    #
    # link += subprocess.check_output(["python", path])

    # r = requests.get("https://codeshare.io/new", allow_redirects=False).text
    # l+ r.split(" ")[-1]
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
    print open(file_path).readline()
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
    print("IN LOGOUT")
    if session['type'] == 'TA':
        TA.set_ta_status(session['net_id'],"offline")
    TA.clear_ta_queue(session['net_id'])
    name = session["name"]
    session.clear()
    return jsonify({"name":name})
    # return flask.redirect('/')
