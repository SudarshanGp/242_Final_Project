import os

from database import TA
# from a import *
from flask import render_template, request, redirect, url_for
from flask_socketio import *
from database import student

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


@main.route('/chat/')
def chat():
    """
    Routed to /chat/ by from landing_page on successful form submission
    chat() retrieves netID and chatID from session and validates whether it is valid
    If valid, it renders chat.html
    :return: Renders chat.html
    """
    netID = session.get('netID', '')
    chatID = session.get('chatID', '')
    if netID == '' or chatID == '':
        return redirect(url_for('.landing'))
    return render_template('chat.html', netID=netID, chatID=chatID,login_status = check_login_status())


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
        return flask.redirect('/'+session['type']+'/'+str(form.net_id.data))

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
            message = "File has been uploaded!"
        else:
            message = "No file to upload!"
    return render_template("instructor.html", message = message,login_status = check_login_status())


@main.route('/Logout/', methods = ["GET", "POST"])
def logout():
    """
    At logout, changes sessions variables
    :return: None
    """
    if session['type'] == 'TA':
        TA.set_ta_status(session['net_id'],"offline")
    session.clear()
    return flask.redirect('/')
