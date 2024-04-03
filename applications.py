from flask import Blueprint, render_template, flash, redirect, url_for
from models import Application, Benefit, db
from flask_login import login_required, current_user

applications_bp = Blueprint('applications', __name__, template_folder='templates')

@applications_bp.route('/apply/<int:benefit_id>', methods=['GET', 'POST'])
@login_required
def apply(benefit_id):
    benefit = Benefit.query.get_or_404(benefit_id)
    application = Application(user_id=current_user.id, benefit_id=benefit_id)
    db.session.add(application)
    db.session.commit()
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('benefits.list_benefits'))

@applications_bp.route('/my-applications')
@login_required
def my_applications():
    applications = current_user.applications.all()
    return render_template('applications.html', applications=applications)