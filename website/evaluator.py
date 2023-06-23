from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from website.models import Project, ProjectStatus

evaluator = Blueprint('evaluator', __name__)

# TODO route per i projects con def metodi crud:
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
    # get projects
    projects = Project.query.all()
    return render_template('evaluator/home.html', user=current_user, projects=projects, project_states=ProjectStatus)


@evaluator.route('/project', methods=['GET', 'POST'])
@login_required
def view_project():
    project_id = request.args.get('project_id')

    # TODO fetch project from db with projct_id from request
    project = {
        "id": 13,
        "name": "Isola delle rose",
        "description": "Isola di metallo senza regole fuori dai confini italiani.",
        "researcher": {
            id: 3242,
            "name": "Mario Rossi",
            "username": "mariorossi"
        },
        "documents": [{"id": 0, "name": "leggi.pdf"}, {"id": 1, "name": "costituzione.pdf"}, {"id": 2, "name": "infrastruttura.pdf"}]
    }

    return render_template('evaluator/project.html', user=current_user, project=project, project_id=project_id)
