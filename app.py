from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from models import db, User #240414 추가

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'
\
db.init_app(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# 블루프린트 등록
from auth import auth_bp
app.register_blueprint(auth_bp)
from benefits import benefits_bp
app.register_blueprint(benefits_bp)
from applications import applications_bp
app.register_blueprint(applications_bp)
from announcements import announcements_bp
app.register_blueprint(announcements_bp)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)