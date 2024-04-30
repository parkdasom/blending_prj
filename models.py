from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'

db = SQLAlchemy(app)

db = SQLAlchemy()

class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    applications = db.relationship('Application', backref='user', lazy='dynamic')
    user_info = db.relationship('UserInfo', uselist=False, backref='user')
    last_notification_checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
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
    income = db.Column(db.Float)
    family_members = db.Column(db.Integer)
    applications = db.relationship('Application', backref='benefit', lazy='dynamic')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Application(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefit.id'), nullable=False)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='승인 대기')

class Announcement(UserMixin, ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Notification {self.content[:20]}...>'

def create_notification(user, benefit_id):
    with current_app.app_context():
        benefit = Benefit.query.get(benefit_id)
        if not benefit:
            return

        content = f"복지 혜택 '{benefit.name}'이(가) 업데이트되었습니다."
        users = User.query.filter(
            (User.income >= benefit.income) & (User.family_members >= benefit.family_members)
        ).all()

        for user in users:
            notification = Notification(content=content, user=user)
            db.session.add(notification)

        user.last_notification_checked_at = datetime.utcnow()  # 마지막 알림 확인 시간을 업데이트
        db.session.commit()