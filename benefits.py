from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Benefit, Notification, create_notification, db
from datetime import datetime

benefits_bp = Blueprint('benefits', __name__, template_folder='templates')

@benefits_bp.route('/benefits', methods=['GET'])
@login_required
def list_benefits():
    income = request.args.get('income', type=float)
    family_members = request.args.get('family_members', type=int)
    if income and family_members:
        benefits = Benefit.query.filter(
            Benefit.income >= income,
            Benefit.family_members >= family_members
        ).order_by(Benefit.id.desc()).all()
    else:
        benefits = Benefit.query.all()

    # 새로운 알림만 가져오기
    notifications = current_user.notifications.filter(
        Notification.created_at > current_user.last_notification_checked_at
    ).all()

    #flash('알림을 확인했습니다.', 'success')  # 알림 확인 메시지 추가

    return render_template('benefits.html', benefits=benefits, notifications=notifications)


@benefits_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    last_checked_at = current_user.last_notification_checked_at
    notifications = Notification.query.filter(
        Notification.user_id == current_user.id,
        Notification.created_at > last_checked_at
    ).all()
    return jsonify([{'id': n.id, 'content': n.content} for n in notifications])

@benefits_bp.route('/notifications/check', methods=['POST'])
@login_required
def check_notifications():
    current_user.last_notification_checked_at = datetime.utcnow()
    db.session.commit()
    #flash('알림을 확인했습니다.', 'success')  # 수정된 부분
    return redirect(url_for('benefits.list_benefits'))


@benefits_bp.route('/benefits/<int:benefit_id>', methods=['PUT'])
@login_required
def update_benefit(benefit_id):
    benefit = Benefit.query.get_or_404(benefit_id)
    data = request.get_json()
    benefit.name = data.get('name', benefit.name)
    benefit.description = data.get('description', benefit.description)
    benefit.requirements = data.get('requirements', benefit.requirements)
    benefit.income = data.get('income', benefit.income)
    benefit.family_members = data.get('family_members', benefit.family_members)
    db.session.commit()

    create_notification(benefit_id)  # 알림 생성 함수 호출

    flash('복지 혜택이 업데이트되었습니다.', 'success')
    return redirect(url_for('benefits.list_benefits'))