from flask import Blueprint, render_template
from flask_login import login_required, current_user

evaluator = Blueprint('evaluator', __name__)

@evaluator.route('/', methods=['GET', 'POST'])
@login_required
def evaluator_home():
    return "welcome home evaluator"