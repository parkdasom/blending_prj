from flask_socketio import emit, join_room, leave_room
from models import Announcement, Application
from app import socketio

# 공지사항 업데이트 시 이벤트 발생
@socketio.on('announcement_posted')
def handle_announcement(data):
    announcement = Announcement.query.get(data['id'])
    emit('new_announcement', {'title': announcement.title, 'content': announcement.content}, broadcast=True)

# 신청 상태 변경 시 이벤트 발생
@socketio.on('application_status_changed')
def handle_application_status(data):
    application = Application.query.get(data['id'])
    emit('status_changed', {'id': application.id, 'status': application.status}, room=application.user.id)

# 사용자 연결 시 방 join
@socketio.on('connect')
def handle_connect():
    join_room(current_user.id)

# 사용자 연결 해제 시 방 leave
@socketio.on('disconnect')
def handle_disconnect():
    leave_room(current_user.id)