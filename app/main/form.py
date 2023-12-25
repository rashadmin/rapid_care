from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,EmailField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from app.models import User


class Chatbot(FlaskForm):
    message = TextAreaField('Enter Message',validators=[DataRequired(),Length(min=3,max=20)])
    submit = SubmitField('Submit Chat')

class NewChat(FlaskForm):
    send = SubmitField('New Chat')

class Edit_Profile(FlaskForm):
    bloodgroup = SelectField('Select Blood Group',choices=[('a_positive','A+'),('a_negative','A-'),('b_positive','B+'),('b_negative','B-'),
                                                           ('ab_positive','AB+'),('ab_negative','AB-'),('o_positive','O+'),('o_negative','O-')]
                                                           ,validators=[])
    genotype = SelectField('Select Genotype',choices=['AA','AS','AC','SS','SC'],validators=[DataRequired()])
    medical_history = TextAreaField('Enter Medical History your Doctor should Know')
    submit = SubmitField('Submit')