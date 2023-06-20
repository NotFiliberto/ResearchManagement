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
