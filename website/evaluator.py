from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from .researcher import CustomResearcher, CustomDocuments, print_Projects

from website.models import Project, ProjectStatus, Researcher, Document

class CustomProject:
    def __init__(self, project_id, name, description, status, researcher, documents):
        self.id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.researcher = researcher
        self.documents = documents

def get_Evaluator_Project(project_id):

    p = Project.query.filter_by(project_id=project_id).first()
    r = Researcher.query.filter_by(id=p.researcher_id).first()
    docs = Document.query.filter_by(project_id=project_id)

    researcher = CustomResearcher(r_id=r.id, name=r.email, username=r.username)
    documents = []
    for d in docs:
        documents.append( CustomDocuments(d_id=d.document_id, name=d.file_name) )
    
    project = CustomProject(project_id=p.project_id, name=p.name, description=p.description, status=ProjectStatus.SUBMITTED_FOR_EVALUATION, 
                            researcher=researcher, 
                            documents=documents)

    return project




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
        # TODO fetch project from db with projct_id from request
        project = get_Evaluator_Project(project_id)

        return render_template('evaluator/evaluate_project.html', user=current_user, project=project, project_statuses=ProjectStatus)
    if request.method == "POST":
        flash("ok valutato", category="success")
        print("\n\nID: ", project_id)
        project = get_Evaluator_Project(project_id)
        return render_template('evaluator/evaluate_project.html', user=current_user, project=project, project_statuses=ProjectStatus)
