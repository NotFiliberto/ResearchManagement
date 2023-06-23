import os
from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Flask
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Document
from werkzeug.utils import secure_filename
from .utils import restrict_user, get_Researcher_Project




researcher = Blueprint('researcher', __name__)


# home
@researcher.route('/',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Researcher")  # TODO: FIX SIGN IN
def researcher_home():
    # testing

    
    # get all project based on user id
    class zzz_project:
        def __init__(self, id, name, description, status):
            self.id = id
            self.name = name
            self.description = description
            self.status = status
    projects = []
    projects.append(zzz_project(
        0, "Nome Progetto", "questa la descrizione inutile di questo progetto", ProjectStatus.NOT_APPROVED))
    projects.append(zzz_project(
        1, "l'isola di piume", "qsdafadsfadsf o", ProjectStatus.SUBMITTED_FOR_EVALUATION))
    projects.append(zzz_project(
        2, "napoli", "che dire follettini", ProjectStatus.REQUIRES_CHANGES))
    projects.append(zzz_project(
        3, "Spalletti's Town", "Uomini forti, destini forti, uomini deboli, destini deboli", ProjectStatus.APPROVED))

    # pretty print projects
    for project in projects:
        print(str(project.__dict__))

    return render_template('researcher/home.html', user=current_user, projects=projects, project_statuses=ProjectStatus)


@researcher.route('/create', methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Researcher")
def create_project():

    if request.method == "GET":
        return render_template('researcher/create.html', user=current_user)
    
    if request.method == "POST":
        # HOW TO LOAD A FILE CORRECTLY: CLICK 'Updload a file' and 
        # then SELECT all the files you need to load
        # Files must be PDF's and you can't select 1 by one, otherwise, counter will fail

        # Saving data request form into DB Project
        project_name = request.form.get('project_name')
        project_description = request.form.get('description')

        # Creating DB Project (ATTENTION EV_INTERVAL=1 TEMPORARY VALUE TESTING)
        project = Project(name=project_name, description=project_description, evaluation_interval_id=1,
                          researcher_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        
        # Check number of uploading files
        files = request.files.getlist("files")
        file_str = str(files)
        # print(file_str)
        num_files = len(files)
        if num_files > 0 and file_str.count("FileStorage: ''") != 1:
            # print("Numero file da caricare: ", num_files)
            flash("Numero di file da caricare: " + str(num_files), category='success')
        else:
            flash("Nessun file da caricare", category="error")
            return redirect(url_for('researcher.create_project'))

        pdf_files = 0
        # CHeck all files extension (PDF)
        for file in files:
            extension = os.path.splitext(file.filename)[1]
            if extension.lower() != '.pdf':
                flash('Caricare solo file PDF, n. pdf inseriti: ' + str(pdf_files) + ' su ' + str(num_files), category='error')
                return render_template('researcher/create.html', user=current_user)
            pdf_files += 1

        # Iterate each file in the files List and save them
        i = 0
        total = num_files
        for file in files:
            # Wether a file si valid and was uploaded inside the form (files)
            if len(file.filename) == 0:
                # flash error on /researcher/create.html
                flash('Questo file non è stato caricato', category='error')
            else:

                filename = secure_filename(file.filename)
                folder_save_into = 'project_files'

                sub_folder = str(project.project_id)
                # sub_folder = str(1) # for TEST change to id = 1, avoiding new dir(None)
                path_save_into = os.path.join(folder_save_into, sub_folder)
                if not os.path.exists(path_save_into):
                    os.makedirs(path_save_into)

                path_to_file = os.path.join(path_save_into, filename)
                if os.path.exists(path_to_file):
                    flash('Il file: ' + str(filename) + ', esiste già nel progetto', category='error')
                    continue

                # Create a document only if file does not already exists
                document = Document(file_extension=extension, file_name=file.filename, project_id=project.project_id)
                # ADD Document into DB
                db.session.add(document)
                db.session.commit()

                file.save(os.path.join(path_save_into, filename))
                i += 1
                
    flash('Progetto creato con successo: ', category='success')
    flash(str(i) + " di " + str(total) + " file inseriti nel progetto", category='success')

    return render_template('researcher/create.html', user=current_user)


@researcher.route('/project', methods=['GET', 'POST'])
@login_required
def get_project():

    project_id = request.args.get('project_id')
    project = get_Researcher_Project(project_id)
    
    return render_template('researcher/project.html', user=current_user, project=project)


