import os

from sqlalchemy import or_
from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Flask
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Document
from werkzeug.utils import secure_filename
from .utils import restrict_user, get_project, re_upload, change_project_state


researcher = Blueprint('researcher', __name__)


# home
@researcher.route('/',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Researcher")  # TODO: FIX SIGN IN
def researcher_home():
    projects = Project.query.filter_by(
        researcher_id=current_user.id).order_by(Project.project_id.desc())
    return render_template('researcher/home.html', user=current_user, projects=projects, project_statuses=ProjectStatus)


@researcher.route('/create', methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Researcher")
def create_project():
    if request.method == "GET":
        return render_template('researcher/create.html', user=current_user)
    if request.method == "POST":
        # Attention: SELECT all the files (.pdf) you need to load ALL AT ONCE -> DON'T DRAG DROP

        # Saving data request form into DB Project
        project_name = request.form.get('project_name')
        project_description = request.form.get('description')
        # Check number of uploading files
        files = request.files.getlist("files")
        file_str = str(files)
        # guarentee that at least one file has been selected for loading
        num_files = len(files)
        if num_files == 0 or file_str.count("FileStorage: ''") == 1:
            flash("Nessun file inserito", category="error")
            return redirect(url_for('researcher.create_project'))

        pdf_files = 0
        # CHeck all files extension (PDF)
        for file in files:
            extension = os.path.splitext(file.filename)[1]
            if extension.lower() != '.pdf':
                flash('Caricare solo file PDF, n. pdf selezionati: ' +
                      str(pdf_files) + ' su ' + str(num_files), category='error')
                return render_template('researcher/create.html', user=current_user)
            pdf_files += 1
        # Creating DB Project (ATTENTION EV_INTERVAL=None -> TESTING PURPOSES)
        project = Project(name=project_name, description=project_description,
                          evaluation_interval_id=None, status=ProjectStatus.SUBMITTED_FOR_EVALUATION,
                          researcher_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        # Iterate each file in the files List and save them
        i = 0
        total = num_files
        for file in files:
            # get filename
            filename = secure_filename(file.filename)
            folder_save_into = 'project_files'
            sub_folder = str(project.project_id)
            # sub_folder = str(1) # for TEST change to id = 1, avoiding new dir(None)
            path_save_into = os.path.join(folder_save_into, sub_folder)
            if not os.path.exists(path_save_into):
                os.makedirs(path_save_into)
            # create path to the file
            path_to_file = os.path.join(path_save_into, filename)
            if os.path.exists(path_to_file):
                flash('Il file: ' + str(filename) +
                      ', esiste già nel progetto', category='error')
                continue
            # Create a document only if file does not already exists, then ADD into DB
            document = Document(
                file_extension=extension, file_name=file.filename, project_id=project.project_id)
            db.session.add(document)
            db.session.commit()
            # save file in the right folder
            file.save(os.path.join(path_save_into, filename))
            i += 1
    # here means that everything was loaded correctly
    flash('Progetto creato con successo: ', category='success')
    flash(str(i) + " di " + str(total) +
          " file caricati correttamente", category='success')
    return render_template('researcher/create.html', user=current_user)


@researcher.route('/project/', methods=['GET'])
@login_required
@restrict_user(current_user, "Researcher")
def view_project():
    
    project_id = request.args.get('project_id')
    project = get_project(project_id)

    if project is None:
        flash('Non esistono progetti corrispondenti nel DB', category='error')
        return redirect(url_for('researcher.researcher_home'))
    else:
        return render_template('researcher/project.html', user=current_user, project=project, project_statuses=ProjectStatus)


@researcher.route('/re_upload', methods=["POST"])
@login_required
@restrict_user(current_user, "Researcher")
def re_upload_documents():
    # get needed data from request
    files = request.files.getlist('files')
    project_id = request.form.get('project_id')
    project = get_project(project_id)
    file_str = str(files)
    num_files = len(files)
    # check if any file was selected
    if num_files == 0 or file_str.count("FileStorage: ''") == 1:
        flash("Nessun file inserito", category="error")
        return redirect(url_for('researcher.view_project', project_id=project_id))
    # check if selected files have a filename that matched
    # with one or more documents of that particular project
    docs = []
    for file in files:
        filename = file.filename
        doc = Document.query.filter_by(
            file_name=filename, project_id=project_id).first()
        if doc is not None:
            docs.append(doc)
        else:
            flash('Uno o più file selezionati non sono validi, ripetere la procedura', category='error')
            return redirect(url_for('researcher.view_project', project_id=project_id))
            # here code means that all the files selected are suitable for reload
    i = 0
    for file in files:
        file_path = re_upload(docs[i])
        file.save(file_path)
        i += 1
    flash('Tutti i file selezionati sono stati ricaricati correttamente',
        category='success')
    project = change_project_state(ProjectStatus.SUBMITTED_FOR_EVALUATION, project)
    return redirect(url_for('researcher.view_project', project_id=project_id))