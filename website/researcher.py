from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

researcher = Blueprint('researcher', __name__)


# home
@researcher.route('/',  methods=['GET', 'POST'])
@login_required
def researcher_home():
    return render_template('researcher/home.html', user=current_user)


# create project page
@researcher.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == "GET":
        return render_template('researcher/create.html', user=current_user)
