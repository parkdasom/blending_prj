from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'

db = SQLAlchemy(app)

db = SQLAlchemy()

class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
"""
class User(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    applications = db.relationship('Application', backref='user', lazy='dynamic')
"""

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    applications = db.relationship('Application', backref='user', lazy='dynamic')
    user_info = db.relationship('UserInfo', uselist=False, backref='user')

    # Flask-Login 요구 속성 추가
    is_active = True  # 기본적으로 활성화된 상태로 설정

    def get_id(self):
        return str(self.id)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    income = db.Column(db.Float)
    family_members = db.Column(db.Integer)
    
class Benefit(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    applications = db.relationship('Application', backref='benefit', lazy='dynamic')

class Application(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefit.id'), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')

class Announcement(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
