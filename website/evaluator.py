from flask import Blueprint, render_template
from flask_login import login_required, current_user

evaluator = Blueprint('evaluator', __name__)


# home
@evaluator.route('/',  methods=['GET', 'POST'])
@login_required
def evaluator_home():
    return render_template('evaluator/home.html', user=current_user)
