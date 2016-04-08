from wtforms import Form, RadioField, PasswordField, validators
from flask.ext.wtf import Form as form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class RegistrationForm(Form):
    """
    @author: Aadhya
    A registration form which allows the user to add name, username, net_id and password
    where there are conditions to check that the repeated password is the same as the original
    password
    """
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    net_id = StringField('Net ID', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')  # makes sure that passwords match
    ])
    confirm = PasswordField('Repeat Password')
    instructor_type = RadioField('Register as', choices=[('TA', 'Teaching Assistant'), ('student', 'Student')])



class LoginForm(Form):
    """
    @author: Aadhya
    A login form which allows a user to login depending upon whether he is a TA or a student
    """
    instructor_type = RadioField('Login as', choices=[('TA', 'Teaching Assistant'), ('student', 'Student')])
    username = StringField('Username')
    password = PasswordField('Password')


class ChatForm(form):
    """
    @author Sudarshan
    Form that takes in a netID and a room ID to start a chat and a submit field which allows a user to submit the
    form
    """
    netID = StringField('NetID', validators=[DataRequired()])
    chatID = StringField('chatID', validators=[DataRequired()])
    submit = SubmitField('Initiate chat')
