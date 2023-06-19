from flask import Blueprint, render_template
from flask_login import login_required, current_user

researcher = Blueprint('researcher', __name__)

@researcher.route('/', methods=['GET', 'POST'])
@login_required
def researcher_home():
    return "welcome home researcher"

