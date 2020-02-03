from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateTimeLocalField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'ed024175621758ad65b836a61cbee9dc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


#Form Model
class LoginForm(FlaskForm, UserMixin):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember', default=False)
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    birthdate = DateField('Date of Birth', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

#Database Model
class tblUser(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)

class tblPost(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.String(36), db.ForeignKey('tbl_user.id'), nullable=False)


from app import route