from .models import Project, Researcher, Document, ProjectStatus, Evaluation_Interval, Report
from flask import redirect, flash, render_template, url_for
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
