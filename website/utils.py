import os
from .models import Project, Researcher, Document, ProjectStatus, Evaluation_Interval, Report
from flask import redirect, url_for
from functools import wraps
from collections import namedtuple
from . import db


def get_project(project_id):
    p = Project.query.filter_by(project_id=project_id).first()
    r = Researcher.query.filter_by(id=p.researcher_id).first()
    docs = Document.query.filter_by(project_id=project_id)

    P = namedtuple('P', ['id', 'name', 'description',
                   'status', 'researcher', 'documents'])
    R = namedtuple('R', ['id', 'name', 'username'])
    D = namedtuple('D', ['id', 'name'])

    res = R(id=r.id, name=r.email, username=r.username)

    documents = []
    for d in docs:
        dd = D(id=d.document_id, name=d.file_name)
        documents.append(dd)

    project = P(id=p.project_id,
                name=p.name,
                description=p.description,
                status=ProjectStatus.SUBMITTED_FOR_EVALUATION,
                researcher=res,
                documents=documents
                )

    return project


# restrict access to pages with this route decorator
def restrict_user(current_user, user_type):
    def decorator(route_function):
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            if not current_user or not current_user.__class__.__name__ == str(user_type):
                return redirect(url_for('static', filename='401.html'))
            return route_function(*args, **kwargs)
        return decorated_function
    return decorator


def create_report(document_id, evaluator_id, description):
    report = Report(document_id=document_id, 
                    evaluator_id=evaluator_id, 
                    description=description)
    db.session.add(report)
    db.session.commit()

    return report


def download_document(document_id):
    d = Document.query.filter_by(document_id=document_id).first()
    file_name = d.file_name
    file_name = file_name.replace(" ", "_")
    sub = str(d.project_id)
    # current path (.py file is stored in website folder)
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Absolute path outside current path(website) -> current path - 1 
    outside_website = os.path.dirname(current_path)
    # Folder name of which contains all the projects
    file_folder_name = 'project_files'
    # path to the folder 
    folder_outside = os.path.join(outside_website, file_folder_name) 
    # path to the subfolder
    subfolder_path = os.path.join(folder_outside, sub)
    # path to file
    file_path = os.path.join(subfolder_path, file_name)
    # return the file path and ONY then you can send the file as a return 
    return file_path

