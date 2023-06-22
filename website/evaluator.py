from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

evaluator = Blueprint('evaluator', __name__)

#TODO route per i projects con def metodi crud: 
#  create(idProgetto, ricercatore), read(ricercatore, valutatore), update, delete  (crud operations)
# sempre controllare che chi fa un'operazione debba essere loggato (prima)
# per fare create -> /root/create : se il metodo è GET reinderizzi sulla pagina createProject.html
# se il metodo è POST (if requested.method == "POST"), returno la stringa che
#  il progetto è stato creato con successo
# tutte  le route sono renderizzate da una cartella apposita fuori da website 

# home
@evaluator.route('/',  methods=['GET', 'POST'])
@login_required
def evaluator_home():
<<<<<<< HEAD
    return render_template('evaluator/home.html', user=current_user)
=======
    return render_template('evaluator/home.html', user=current_user, projects=[])


@evaluator.route('/project', methods=['GET', 'POST'])
@login_required
def view_project():
    project_id = request.args.get('project_id')

    return render_template('evaluator/project.html', user=current_user, project_id=project_id)
>>>>>>> b79aadeaedd777e0f196056f5e42518db0d9ba0f
