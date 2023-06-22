import os
import shutil
from flask import Blueprint, Flask, app, render_template, request, flash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Evaluation_Interval, Researcher, Document
from werkzeug.utils import secure_filename
from . import db
import datetime


def read_project(project_id):
    p = Project.query.filter_by(project_id=project_id).first()
    # making a list of the project info
    project_info = [p.project_id, p.name, p.status,
                    p.researcher_id, p.evaluation_interval_id]
    interval = Evaluation_Interval.query.filter_by(
        evaluation_interval_id=p.evaluation_interval_id).first()
    researcher = Researcher.query.filter_by(id=p.researcher_id).first()
    documents = Document.query.filter_by(project_id=p.project_id)
    project_info.append(documents.count())
    for d in documents:
        project_info.append(d)

    project_div = [project_info, [interval.start, interval.end],
                   [researcher.username, researcher.email]]
    return project_div


def restrict_user(current_usr, user_type):
    def decorator(route_function):
        def decorated_function(*args, **kwargs):
            # Check if user is a Researcher
            if not current_usr.__class__.__name__ == str(user_type):
                flash('You need to be a ' + str(user_type) +
                      ' user to access that page', category='error')
                return redirect(url_for('auth.sign_in'))
            return route_function(*args, **kwargs)
        return decorated_function
    return decorator


researcher = Blueprint('researcher', __name__)


# home
@researcher.route('/',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Researcher")
def researcher_home():
    return render_template('researcher/home.html', user=current_user)

@researcher.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == "GET":
        # PRINTS EVERY TIME AS TEST read_project(id) function
        projects = Project.query.all()
        print("Projects here: ", projects)
        for p in projects:
            print(read_project(p.project_id))
        return render_template('researcher/create.html', user=current_user)

    i = 0
    total = 0
    temp = -1
    if request.method == "POST":
        # Saving data request form into DB Project 
        project_name = request.form.get('project_name') 
        # Description handle: description = request.form.get('description')
        if len(request.files.getlist("file")) != 0:
            temp += 1
        print("temp ", temp)
        # All files in load list must be PDF's
        files = request.files.getlist("file")
        
        print("files: ", files)
        
        print("len files: ", len(request.files.getlist('file')))
        
        if len(request.files.getlist('file')) != 0:
            for file in files:
                extension = os.path.splitext(file.filename)[1]
                if extension.lower() != '.pdf':
                    flash('Upload only PDFs', category='error')
                    return render_template('researcher/create.html', user=current_user)
        else:
            flash('No files has been loaded', category='error')
            return render_template('researcher/create.html', user=current_user)

        # Creating DB Project (ATTENTION EV_INTERVAL=1 TEMPORARY VALUE TESTING)
        project = Project(name=project_name, evaluation_interval_id=1,
                          researcher_id=current_user.id)
        db.session.add(project)
        db.session.commit()

        # Iterate each file in the files List and save them 
        for file in files:
            # Wether a file si valid and was uploaded inside the form (files)
            if len(file.filename) == 0:
                # flash error on /researcher/create.html
                flash('No file was loaded', category='error')
            else:
                total += 1
                filename = secure_filename(file.filename)
                folder_save_into = 'project_files'
                sub_folder = str(project.project_id)
                path_save_into = os.path.join(folder_save_into, sub_folder)
                if not os.path.exists(path_save_into):
                    os.makedirs(path_save_into)

                path_to_file = os.path.join(path_save_into, filename)
                if os.path.exists(path_to_file):
                    flash('File already exists', category='error')
                    continue
                # Create a document only if file does not already exists
                document = Document(file_extension=extension, file_name=file.filename, 
                                    topic="default topic", project_id=project.project_id)
                #ADD Document into DB 
                db.session.add(document)
                db.session.commit()
                file.save(os.path.join(path_save_into, filename))
                i += 1
                # tenere conto di quanti ne carica e quali
                
    flash('Project has been successfully created', category='success')
    flash(str(i) + ' of ' + str(total) + ' files has been loaded', category='success')
    return render_template('researcher/home.html', user=current_user)
