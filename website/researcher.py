import os
import shutil
from flask import Blueprint, Flask, app, render_template, request, flash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Evaluation_Interval, Researcher, Document
from werkzeug.utils import secure_filename
from . import db
import datetime

# creare una cartella specificando dove e con che nome
def crea_cartella(cartella_padre, nome_nuova_cartella):
    percorso_nuova_cartella = os.path.join(cartella_padre, nome_nuova_cartella)
    os.mkdir(percorso_nuova_cartella)


# prendere un file e metterlo dentro una cartella specificando il nome
def move_file_into(file_da_spostare, cartella_destinazione):
    shutil.move(file_da_spostare, cartella_destinazione)
    print(f"Il file '{file_da_spostare}' è stato spostato nella cartella '{cartella_destinazione}' con successo.")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# allowed files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def researcher_only(route_function):
    def decorated_function(*args, **kwargs):
        # Verifica se l'utente corrente è un ricercatore
        if not current_user.__class__.__name__ == "Researcher":
            return redirect(url_for('researcher.researcher_home'))  # Reindirizza all'home dei ricercatori
        return route_function(*args, **kwargs)
    return decorated_function


researcher = Blueprint('researcher', __name__)

#TODO route per i projects con def metodi crud: 
#  create(idProgetto, ricercatore), read(ricercatore, valutatore), update, delete  (crud operations)
# sempre controllare che chi fa un'operazione debba essere loggato (prima)
# per fare create -> /root/create : se il metodo è GET reinderizzi sulla pagina createProject.html
# se il metodo è POST (if requested.method == "POST"), returno la stringa che
#  il progetto è stato creato con successo
# tutte  le route sono renderizzate da una cartella apposita fuori da website 


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
        return render_template('researcher/create.html', user=current_user)

    if (request.method == "POST"):

        # Saving data request form into DB Project 
        project_name = request.form.get('project_name') 
        description = request.form.get('description')
        print("project info -> name: " + project_name + " description: " + description + " researcher_id: " + str(current_user.id))

        # Creating DB Project (no description -> add it to the document topic? OR add id to Project model?)
        project = Project(name=project_name, researcher_id=current_user.id)
        #db.session.add(project)
        #db.session.commit()


        # Get the list of files from webpage
        # print('UPLOAD???')
        files = request.files.getlist("file")
        print(files)

        # Iterate for each file in the files List, and Save them (non li scorre tutti bro, solo 1 bro)
        i = 0
        for file in files:
            print("file ", i, " -->  filename ", file.filename, " , length filename ", len(file.filename))
            # Wether a file si valid and was uploaded inside the form (files)
            if len(file.filename) == 0:
                print('no files loaded')
                flash('No file was loaded', category='error')
            else:
                extension = os.path.splitext(file.filename)[1]
                if extension.lower() != '.pdf':
                    print("ONLY PDFS")
                    flash('Upload only PDFs', category='error')
                    return redirect(url_for('researcher.researcher_home'))
                document = Document(file_extension=extension, file_name=file.filename, 
                                    topic=description, project_id=project.project_id)
                project.project_id = 2
                print("extension: ", extension, " project_id: ", project.project_id)
                #db.session.add(document)
                #db.session.commit()

                filename = secure_filename(file.filename)

                folder_save_into = 'project_files'
                sub_folder = str(project.project_id)

                path_save_into = os.path.join(folder_save_into, sub_folder)
                if not os.path.exists(path_save_into):
                    os.makedirs(path_save_into)

                path_to_file = os.path.join(path_save_into, filename)
                if os.path.exists(path_to_file):
                    print("File already exists in the destination folder")
                    flash('File already exists', category='error')
                    return redirect(url_for('researcher.researcher_home'))

                file.save(os.path.join(path_save_into, filename))
                
                print('Files loaded correctly')
                flash('Files loaded', category='success')
                i += 1
    

    return render_template('researcher/create.html', user=current_user)
