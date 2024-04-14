from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User


class NewBusinessForm(FlaskForm):
    title = StringField('Name of the Business', validators=[DataRequired(), Length(min=1, max=30)])
    contact = StringField('Contact details', validators=[DataRequired(), Length(min=1, max=30)])
    text = StringField('Extra information', validators=[DataRequired(), Length(min=1, max=30)])
    submit = SubmitField('Submit')


class NewUserForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail address', validators=[DataRequired(), Email(message='The e-mail address does not meet the criteria.')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirming password', validators=[DataRequired(),
                                     EqualTo('password', message='The confirming password does not match.')])
    submit = SubmitField('register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This e-mail adress is already taken. Please choose another!')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Stay logged in')
    submit = SubmitField('Log in')
