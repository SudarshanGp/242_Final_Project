from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect, url_for
from flask_socketio import *
from TA import *
from student import *
from VOH.main.forms import RegistrationForm, LoginForm, ChatForm
from authentication import *
from . import main
from .. import app
import os

"""
    views.py is in charge of routing different server requests from clients.

"""

@main.route('/')
@main.route('/index/')
def main_page():
    """
    Routed to main_page() on load of website
    Renders base.html
    """
    return render_template("base.html")


@main.route('/chat/')
def chat():
    """
    @author: Sudarshan
    Routed to /chat/ by from landing_page on successful form submission
    chat() retrieves netID and chatID from session and validates whether it is valid
    If valid, it renders chat.html
    """
    netID = session.get('netID', '')
    chatID = session.get('chatID', '')
    if netID == '' or chatID == '':
        return redirect(url_for('.landing'))
    return render_template('chat.html', netID=netID, chatID=chatID)


@main.route('/login/')
def login():
    """
    @author: Aadhya
    Login Page
    :return: Template
    """
    form = LoginForm()
    return render_template("login.html", form = form)


@main.route('/register/')
def register():
    """
    @author: Aadhya
    Registration Page
    :return: Template
    """
    form = RegistrationForm()
    return render_template("register.html", form = form)


@main.route('/register/', methods=["POST"])
def register_user():
    """
    @author: Nihal
    :return: None
    """
    # Get the Form
    form = RegistrationForm(request.form)
    # Validate the Form
    if request.method == "POST" and form.validate():
        # Register TA
        print form
        if form.instructor_type.data == "TA":
            # "Adding TA"
            add_TA(form.username.data, form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)
        elif form.instructor_type.data == "student":
            # "Adding student"
            add_student(form.username.data, form.password.data, form.name.data, form.net_id.data, form.instructor_type.data)
    # Return a new form
    form = RegistrationForm()
    return render_template("register.html", form = form)


@main.route('/authenticate/', methods=["POST"])
def authenticate_login():
    """
    @author: Nihal
    Authenticate Login
    """
    # Get Login Form
    form = LoginForm(request.form)
    # Authenticate USER
    if authenticate_user(form.username.data, form.password.data, form.instructor_type.data):
        # Redirect to main Landing
        return flask.redirect('/landing/'+str(form.username.data))
    # Error! Redirect to Login Page
    return flask.redirect('/login/')


@main.route('/landing/<user>', methods=['GET', 'POST'])
def landing_page(user):
    """
    @author: Sudarshan
    Landing Page after Login for a particular user
    landing_page() validates the form submission and redirects to /chat/ if it is successful form POST
    :param user: NetID of user
    """
    form = ChatForm()  # Create a form as an instance of ChatFrom class
    if form.validate_on_submit(): # On submission of From
        session['netID'] = form.netID.data # Get NetID
        session['chatID'] = form.chatID.data # Get unique chatID
        return redirect(url_for('.chat')) # Redirect to /chat/
    elif request.method == 'GET': # If its a get request
        form.netID.data = session.get('netID', '') # Retrieve netID from form
        form.chatID.data = session.get('chatID', '') # Retrieve chatID from form
    return render_template("landing.html", netid = user, form = form ) # Render landing page


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

