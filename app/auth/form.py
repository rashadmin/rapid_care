from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from app.models import User

class Login(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Register(FlaskForm):
    firstname = StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    lastname = StringField('Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='Password must be Equal to each other'),Length(min=4,max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist!!!, Pick another.')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Address already exist!!!, Pick another.')