from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields import StringField, SubmitField, PasswordField, BooleanField


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(4, 25)])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Password must match'),
                                                     Length(min=8)])
    confirm = PasswordField('Repeat password')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


