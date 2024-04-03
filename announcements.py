from flask import Blueprint, render_template
from models import Announcement

announcements_bp = Blueprint('announcements', __name__, template_folder='templates')

@announcements_bp.route('/announcements')
def list_announcements():
    announcements = Announcement.query.all()
    return render_template('announcements.html', announcements=announcements)