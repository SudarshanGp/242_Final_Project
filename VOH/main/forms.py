from wtforms import Form, RadioField, TextField, PasswordField, BooleanField,validators


class RegistrationForm(Form):


    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    instructor_type = RadioField('', choices=[('ta','Teaching Assistant'),('stud','Student')])

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me?')
