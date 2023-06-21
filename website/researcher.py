import os
import shutil
from flask import Blueprint, Flask, app, render_template, request, flash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Evaluation_Interval, Researcher, Document
from werkzeug.utils import secure_filename
from . import db
import datetime
import PyPDF2


def read_project(project_id):
    p = Project.query.filter_by(project_id=project_id).first()
    # making a list of the project info
    project_info = [ p.project_id, p.name, p.status, p.researcher_id, p.evaluation_interval_id]
    interval = Evaluation_Interval.query.filter_by(
    evaluation_interval_id=p.evaluation_interval_id).first()
    researcher = Researcher.query.filter_by(id=p.researcher_id).first()
    documents = Document.query.filter_by(project_id=p.project_id)
    project_info.append(documents.count()) 
    for d in documents:
        project_info.append(d)

    project_div = [project_info, [interval.start, interval.end], [researcher.username, researcher.email]]
    return project_div

def researcher_only(route_function):
    def decorated_function(*args, **kwargs):
        # Check if user is a Researcher
        if not current_user.__class__.__name__ == "Researcher":
            return redirect(url_for('researcher.researcher_home')) 
        return route_function(*args, **kwargs)
    return decorated_function


researcher = Blueprint('researcher', __name__)


# home
@researcher.route('/',  methods=['GET', 'POST'])
@login_required
def researcher_home():
    return render_template('researcher/home.html', user=current_user)

@researcher.route('/create', methods=['GET', 'POST'])
@login_required
@researcher_only
def create_project():

    if request.method == "GET":
        # PRINTS EVERY TIME AS TEST read_project(id) function
        projects = Project.query.all()
        print("Projects here: ", projects)
        for p in projects:
            print(read_project(p.project_id))
        return render_template('researcher/create.html', user=current_user)

    if request.method == "POST":
        # Saving data request form into DB Project 
        project_name = request.form.get('project_name') 
        description = request.form.get('description')

        # Creating DB Project (ATTENTION EV_INTERVAL=1 TEMPORARY VALUE TESTING)
        project = Project(name=project_name, evaluation_interval_id=1,
                           researcher_id=current_user.id)
        db.session.add(project)
        db.session.commit()

        files = request.files.getlist("file")

        # Iterate each file in the files List and save them 
        i = 0
        for file in files:
            # Wether a file si valid and was uploaded inside the form (files)
            if len(file.filename) == 0:
                flash('No file was loaded', category='error')
            else:
                extension = os.path.splitext(file.filename)[1]
                if extension.lower() != '.pdf':
                    flash('Upload only PDFs', category='error')
                    return redirect(url_for('researcher.researcher_home'))
                
                filename = secure_filename(file.filename)
                
                folder_save_into = 'project_files'
                sub_folder = str(project.project_id)

                path_save_into = os.path.join(folder_save_into, sub_folder)
                if not os.path.exists(path_save_into):
                    os.makedirs(path_save_into)

                path_to_file = os.path.join(path_save_into, filename)
                if os.path.exists(path_to_file):
                    flash('File already exists', category='error')
                    return redirect(url_for('researcher.researcher_home'))
                # Create a document only if file does not already exists
                document = Document(file_extension=extension, file_name=file.filename, 
                                    topic=description, project_id=project.project_id)
                #ADD Document into DB 
                db.session.add(document)
                db.session.commit()

                file.save(os.path.join(path_save_into, filename))
                
                flash('Files loaded', category='success')
                i += 1
    
    return render_template('researcher/create.html', user=current_user)


