from flask import Blueprint, render_template, flash, redirect, url_for
from models import Application, Benefit, db, UserInfo, User
from flask_login import login_required, current_user
from forms import UserInfoForm
from sqlalchemy.orm import joinedload

applications_bp = Blueprint('applications', __name__, template_folder='templates')

@applications_bp.route('/apply/<int:benefit_id>', methods=['GET', 'POST'])
@login_required
def apply(benefit_id):
    benefit = Benefit.query.get_or_404(benefit_id)
    application = Application(user_id=current_user.id, benefit_id=benefit_id)
    db.session.add(application)
    db.session.commit()
    flash('복지혜택 신청이 완료 되었습니다.', 'success')
    return redirect(url_for('benefits.list_benefits'))

@applications_bp.route('/my-applications')
@login_required
def my_applications():
    applications = current_user.applications.options(
        joinedload(Application.user).joinedload(User.user_info)
    ).all()
    return render_template('applications.html', applications=applications)

@applications_bp.route('/user-info', methods=['GET', 'POST'])
@login_required
def user_info():
    form = UserInfoForm()
    if form.validate_on_submit():
        user_info = UserInfo(
            user_id=current_user.id,
            income=form.income.data,
            family_members=form.family_members.data
        )
        db.session.add(user_info)
        db.session.commit()
        flash('User information saved successfully!', 'success')
        return redirect(url_for('applications.my_applications'))
    return render_template('user_info.html', form=form)