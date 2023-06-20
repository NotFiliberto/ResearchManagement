import os
import shutil
from flask import Blueprint, Flask, app, render_template, request, flash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Project, ProjectStatus, Evaluation_Interval, Researcher
from werkzeug.utils import secure_filename
from . import db
import datetime

# creare una cartelle col nome del progetto
def crea_cartella(nome_cartella):
    try:
        os.mkdir(nome_cartella)
        print(f"Folder '{nome_cartella}' has been succesfully created")
    except FileExistsError:
        print(f"Folder '{nome_cartella}' already exists.")

# prendere un file e metterlo dentro una cartella specificando il nome
def sposta_file_in_cartella(file_da_spostare, cartella_destinazione):
    try:
        shutil.move(file_da_spostare, cartella_destinazione)
        print(f"Il file '{file_da_spostare}' è stato spostato nella cartella '{cartella_destinazione}' con successo.")
    except FileNotFoundError:
        print(f"Il file '{file_da_spostare}' non esiste.")
    except shutil.Error:
        print(f"Si è verificato un errore nello spostamento del file '{file_da_spostare}'.")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# allowed files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
def create_project():

    if request.method == "GET":
        return render_template('researcher/create.html', user=current_user)
    elif request.method == "POST":	

        #data form
        #db.session.add(Project(evaluation_interval_id=interval.evaluation_interval_id, researcher_id=1))
        
        #data = request.form
        #print(data)

        #ev_interval_id = request.form.get('ev_interval_id')
        #res_id = request.form.get('res_id')

        #project = Project(evaluation_interval_id=ev_interval_id, researcher_id=res_id)

        #documenti da ricevere in input e crearli:
        # creare una cartella nominata con l'id del progetto e dentro ci mettiamo i documenti che 
        # l'utente carica  -> ricevuti dal form

        #crea_cartella(str(Project.query.filter_by(project_id=1).first().project_id))

        # mettere i documenti dentro la cartella creata

        project = Project.query.filter_by(project_id=1).first()

        UPLOAD_FOLDER = str(project.project_id)
        
        

        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # check if the post request has the file part
        if 'file' not in request.files:
            print("file non nelle richieste file")
            flash('No file part', category='error')
            return render_template('researcher/create.html', user=current_user)
       
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print("file senza nome")
            flash('No selected file', category='error')
            return render_template('researcher/create.html', user=current_user)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "sus file uploadato"
            #return redirect(url_for('uploaded_file',filename=filename))

        

        #db.session.add(project)
        #db.session.commit()

        

        flash('Project created', category='success')

    

    return render_template('researcher/create.html', user=current_user)

