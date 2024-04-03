from flask import Blueprint, render_template
from models import Benefit

benefits_bp = Blueprint('benefits', __name__, template_folder='templates')

@benefits_bp.route('/benefits')
def list_benefits():
    benefits = Benefit.query.all()
    return render_template('benefits.html', benefits=benefits)