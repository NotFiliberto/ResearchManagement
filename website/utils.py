from .models import Project, Researcher, Document, ProjectStatus, Evaluation_Interval
from flask import redirect, flash, url_for
from functools import wraps


class CustomProject1:
    def __init__(self, project_id, name, description, researcher, documents):
        self.id = project_id
        self.name = name
        self.description = description
        self.researcher = researcher
        self.documents = documents


class CustomProject2:
    def __init__(self, project_id, name, status, description, researcher, documents):
        self.id = project_id
        self.name = name
        self.status = status
        self.description = description
        self.researcher = researcher
        self.documents = documents


class CustomResearcher:
            def __init__(self, r_id, name, username):
                self.id = r_id
                self.name = name
                self.username = username


class CustomDocuments:
            def __init__(self, d_id, name):
                self.id = d_id
                self.name = name


def r_definition(p, researcher, documents):
    return CustomProject1( project_id=p.project_id, name=p.name, description=p.description, 
                            researcher=researcher,
                            documents=documents)


def e_definition(p, researcher, documents):
    return CustomProject2( project_id=p.project_id, name=p.name, 
                          status=ProjectStatus.SUBMITTED_FOR_EVALUATION, description=p.description, 
                            researcher=researcher,
                            documents=documents)


def get_project(project_id, definition):
    p = Project.query.filter_by(project_id=project_id).first()
    r = Researcher.query.filter_by(id=p.researcher_id).first()
    docs = Document.query.filter_by(project_id=project_id)
    researcher = CustomResearcher(r_id=r.id, name=r.email, username=r.username)
    documents = []
    for d in docs:
        documents.append( CustomDocuments(d_id=d.document_id, name=d.file_name) )
    if definition == "r":
        return r_definition(p, researcher, documents)
    if definition == "e":
        return e_definition(p, researcher, documents)


def restrict_user(current_user, user_type):
    def decorator(route_function):
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            # Check if user is a Researcher
            if not current_user or not current_user.__class__.__name__ == str(user_type):
                flash('You need to be a ' + str(user_type) +
                      ' user to access that page', category='error')
                return redirect(url_for('auth.sign_in'))
            return route_function(*args, **kwargs)
        return decorated_function
    return decorator


def print_projects(s, e):
    projects = Project.query.filter(Project.project_id.between(s, e)).all()
    list_p = []
    for p in projects:
        i = Evaluation_Interval.query.filter_by(evaluation_interval_id=p.evaluation_interval_id).first()
        r = Researcher.query.filter_by(id=p.researcher_id).first()
        list_p.append([ p.project_id, p.name, p.description, p.status, 
                        [i.evaluation_interval_id, i.start, i.end], 
                        [r.id, r.email, r.username] ])
    print("Projects here: ")
    for elem in list_p:
        print(elem)
    return list_p


def read_project(project_id):
    p = Project.query.filter_by(project_id=project_id).first()
    # making a list of the project info
    print("read: ", p, " id: ", project_id)
    project_info = [p.project_id, p.name, p.status,
                    p.researcher_id, p.evaluation_interval_id]
    interval = Evaluation_Interval.query.filter_by(
        evaluation_interval_id=p.evaluation_interval_id).first()
    researcher = Researcher.query.filter_by(id=p.researcher_id).first()
    documents = Document.query.filter_by(project_id=p.project_id)
    project_info.append(documents.count())
    for d in documents:
        project_info.append(d)

    project_div = [project_info, [interval.start, interval.end],
                   [researcher.username, researcher.email]]
    return project_div


