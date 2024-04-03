from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from models import ModelMixin, User, Benefit, Application, Announcement

from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 데이터베이스 생성
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 모델 임포트
from models import User, Benefit, Application, Announcement

# 블루프린트 등록
from auth import auth_bp
app.register_blueprint(auth_bp)

from benefits import benefits_bp
app.register_blueprint(benefits_bp)

from applications import applications_bp
app.register_blueprint(applications_bp)

from announcements import announcements_bp
app.register_blueprint(announcements_bp)

# 소켓 이벤트 핸들러 임포트
from events import *

# 데이터베이스 생성
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)