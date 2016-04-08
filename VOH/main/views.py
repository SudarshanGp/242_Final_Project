from flask import Flask, Blueprint
from flask import render_template, request, session, jsonify, redirect, url_for
from flask_socketio import *
from ta import *
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
    Create a login form and pass that into render_template so as to populate the form
    :return: Template
    """
    form = LoginForm()
    return render_template("login.html", form = form)


@main.route('/register/')
def register():
    """
    @author: Aadhya
    Create a registration form and pass that into render_template so as to populate the form
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
    """
    @author: Aadhya
    Creates an instructor view with added functionality for file uploading with proper message feedback
    :return: template which returns a instructor view along with the message if file upload is successful
    """
    message = "No file uploaded" # Default message in case no file is uploaded
    if request.method == 'POST': # If there is a POST request i.e. a file submit button has clicked then:
        file = request.files['file'] # Get the file which the user has uploaded
        if file: #If the file exists
            filename = file.filename # Get the filename
            path_of_file = "VOH/" + os.path.join(app.config['UPLOAD_FOLDER'], filename) # Path where file is stored
            file.save(path_of_file) # Save the file at the particular path
            message = "File has been uploaded!" # Change the response message
        else:
            message = "No file to upload!" # If the file does not exist then change message
    return render_template("instructor.html", message = message) # Renders the template with the current message

