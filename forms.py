# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class UserInfoForm(FlaskForm): #마이페이지 사용자 정보 입력 폼 생성
    income = FloatField('Income')
    family_members = IntegerField('Number of Family Members')