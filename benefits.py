from flask import Blueprint, render_template, request
from models import Benefit

benefits_bp = Blueprint('benefits', __name__, template_folder='templates')

@benefits_bp.route('/benefits', methods=['GET'])
def list_benefits():
    income = request.args.get('income', type=float) or None
    family_members = request.args.get('family_members', type=int) or None

    query = Benefit.query

    if income is not None:
        query = query.filter(Benefit.income >= income)
    if family_members is not None:
        query = query.filter(Benefit.family_members <= family_members)

    benefits = query.order_by(Benefit.id.desc()).all()

    return render_template('benefits.html', benefits=benefits)

"""
benefits_bp = Blueprint('benefits', __name__, template_folder='templates')

@benefits_bp.route('/benefits')
def list_benefits():
    benefits = Benefit.query.all()
    return render_template('benefits.html', benefits=benefits)
"""