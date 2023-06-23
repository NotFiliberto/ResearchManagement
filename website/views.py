from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)
# view = Blueprint('views', __name__, template_folder='folder/to/template')


@views.route('/',  methods=['GET', 'POST'])
@login_required
def home():
    # conditional redirect based on user type
    if current_user.__class__.__name__ == "Researcher":
        return redirect(url_for('researcher.researcher_home'))
    elif current_user.__class__.__name__ == "Evaluator":
        return redirect(url_for('evaluator.evaluator_home'))
