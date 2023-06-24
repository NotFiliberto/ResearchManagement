from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from website.models import Project, ProjectStatus
from .utils import get_project


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
    return render_template('evaluator/home.html', user=current_user, projects=projects, project_statuses=ProjectStatus)


@evaluator.route('/evaluate_project', methods=['GET', 'POST'])
@login_required
def evaluate_project():

    if request.method == "GET":
        project_id = request.args.get('project_id')
        project = get_project(project_id)

        return render_template('evaluator/evaluate_project.html', user=current_user, project=project, project_statuses=ProjectStatus)
    
    if request.method == "POST":
        flash("ok valutato", category="success")
        project_id = request.form.get('project_id')
        project = get_project(project_id)
        return render_template('evaluator/evaluate_project.html', user=current_user, project=project, project_statuses=ProjectStatus)
