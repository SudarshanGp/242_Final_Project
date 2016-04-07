from wtforms import Form, RadioField, TextField, PasswordField, BooleanField,validators
from flask.ext.wtf import Form as form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required



class RegistrationForm(Form):

    name = TextField('Name', [validators.Length(min=4, max=25)])
    username = TextField('Username', [validators.Length(min=4, max=25)])
    net_id= TextField('Net ID', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    instructor_type = RadioField('Register as', choices=[('TA','Teaching Assistant'),('student','Student')])


class LoginForm(Form):
    instructor_type = RadioField('Login as', choices=[('TA','Teaching Assistant'),('student','Student')])
    username = TextField('Username')
    password = PasswordField('Password')

class ChatForm(form):
    """
        Form that takes in a netID and a room ID to start a chat
    """
    netID = StringField('NetID', validators=[Required()])
    chatID = StringField('chatID', validators=[Required()])
    submit = SubmitField('Initiate chat')
