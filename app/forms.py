from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User

class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
#    pword2 = StringField('2FA', validators=[DataRequired()], id="2fa")
    pword2 = StringField('2FA', id="2fa")
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    pword2 = StringField('2FA', validators=[Regexp("\d{10}|^$")], id="2fa")
    submit = SubmitField('Register')

    def validate_uname(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    post = TextAreaField('Text For Spellcheck Program', validators=[DataRequired(), Length(min=1, max=140)], id="inputtext")
    submit = SubmitField('Submit')

class HistoryForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()], id="userquery")
    submit = SubmitField('Search')

class LoginHistoryForm(FlaskForm):
    uid = StringField('UserID', validators=[DataRequired()], id="userid")
    submit = SubmitField('Search')

