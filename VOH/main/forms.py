from wtforms import Form, RadioField, TextField, PasswordField, BooleanField,validators


class RegistrationForm(Form):

    name = TextField('Name', [validators.Length(min=4, max=25)])
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
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