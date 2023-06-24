from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from website.models import Project, ProjectStatus
from .utils import get_project, restrict_user


evaluator = Blueprint('evaluator', __name__)

# TODO route per i projects con def metodi crud:
#  create(idProgetto, ricercatore), read(ricercatore, valutatore), update, delete  (crud operations)


# home
@evaluator.route('/',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Evaluator")
def evaluator_home():
    # get projects
    projects = Project.query.order_by(Project.project_id.desc()).all()
    return render_template('evaluator/home.html', user=current_user, projects=projects, project_statuses=ProjectStatus)


@evaluator.route('/evaluate_project', methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, "Evaluator")
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
