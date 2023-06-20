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

    if (request.method == "POST"):
        # Get the list of files from webpage
        print('UPLOAD???')
        files = request.files.getlist("file")

        # Iterate for each file in the files List, and Save them
        i = 0
        for file in files:
            print("file --> ", file.filename, i)
            i += 1
        return "ok bro"
