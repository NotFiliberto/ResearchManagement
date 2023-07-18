import io
import os
import zipfile
from website.config import PROJECT_FILES_FOLDER
from .models import Project, Researcher, Document, ProjectStatus, Report, User
from flask import redirect, url_for
from sqlalchemy import MetaData
from functools import wraps
from collections import namedtuple
from . import db
import unicodedata

def standardize_accents(string):
    return ''.join(c for c in unicodedata.normalize('NFD', string) if not unicodedata.combining(c))


# tested, added documents[i].report


def get_project(project_id):
    # Define the models dictionary based on the attributes of the reflected tables
    project_columns = Project.__table__.columns.keys()
    researcher_columns = User.__table__.columns.keys()
    document_columns = Document.__table__.columns.keys()
    report_columns = Report.__table__.columns.keys()
    project = db.session.query(Project).filter_by(project_id=project_id).first()
    if project is None:
        return None
    researcher = db.session.query(Researcher).filter_by(id=project.researcher_id).first()
    res_dict = {key: value for key, value in researcher.__dict__.items() if key in researcher_columns}
    docs = Document.query.filter_by(project_id=project_id)
    documents = []
    for d in docs:
        project_rep = Report.query.filter_by(document_id=d.id).first()
        if project_rep is not None:
            rep_dict = {key: value for key, value in project_rep.__dict__.items() if key in report_columns}
            d_dict = {key: value for key, value in d.__dict__.items() if key in document_columns}
            d_dict['report'] = rep_dict
        else:
            rep_dict = None
            d_dict = {key: value for key, value in d.__dict__.items() if key in document_columns}
            d_dict['report'] = rep_dict
        documents.append(d_dict)

    project_dict = {key: value for key, value in project.__dict__.items() if key in project_columns}
    print("\n\n",res_dict, "\n\n")
    project_dict['researcher'] = res_dict
    project_dict['documents'] = documents

    return project_dict


# tested, usage: restrict access to pages with this route decorator


def restrict_user(current_user, authorized_types):
    def decorator(route_function):
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            authorized = False
            for user_type in authorized_types:
                if current_user.__class__.__name__ == str(user_type):
                    authorized = True
            if authorized == False or current_user is None:
                return redirect(url_for('static', filename='401.html'))
            return route_function(*args, **kwargs)
        return decorated_function
    return decorator

# tested


def change_project_state(status, project):
    if status != project['status']:
        p = Project.query.filter_by(project_id=project['project_id']).first()
        p.status = status
        db.session.commit()
        project = get_project(project['project_id'])
        return project

# tested


def create_report(document_id, evaluator_id, description):
    document = Document.query.filter_by(id=document_id).first()

    if (document is None):  # document not exists
        return None

    # find existing report
    report = Report.query.filter_by(
        document_id=document_id).first()

    # check if already exist
    if report is None:
        # add
        report = Report(document_id=document_id,
                        evaluator_id=evaluator_id,
                        description=description)
        db.session.add(report)
        db.session.commit()
    else:
        # update
        report.description = description

        db.session.commit()

    return report


# tested
def get_reports(project_id):
    p = get_project(project_id)
    reports = []
    for d in p['documents']:
        if d['report'] is not None:
            reports.append(d['report'])

    return reports

# tested -> usage: to get the path of the file so
# you can send_file(path) to the page where it is needed


def download_document(document_id):
    d = Document.query.filter_by(id=document_id).first()
    filename = standardize_accents(d.filename)
    sub = str(d.project_id)
    # current path (.py file is stored in website folder)
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Absolute path outside current path(website) -> current path - 1
    outside_website = os.path.dirname(current_path)
    # path to the folder
    folder_outside = os.path.join(outside_website, PROJECT_FILES_FOLDER)
    # path to the subfolder
    subfolder_path = os.path.join(folder_outside, sub)
    # path to file
    file_path = os.path.join(subfolder_path, filename)
    # return the file path and ONY then you can send the file as a return
    return file_path

# tested
# TEST THIS FUNCTION WITH THIS CODE IN A ROUTE:
#  zip_buffer = download_zip_documents(project_id)
#  name = 'project_{}_files.zip'.format(project_id)
#  return send_file(zip_buffer, as_attachment=True, download_name=name)


def download_zip_documents(project_id):
    p = get_project(project_id)
    file_paths = []
    for d in p['documents']:
        # download_document returns the path of the file so you can download it
        file_paths.append(download_document(d['id']))
       # Create .zip temporary file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for file_path in file_paths:
            # no need to specify the whole path to the file
            file_name = os.path.basename(file_path)
            # Add to .zip file with no other sub-directories
            zipf.write(file_path, arcname=file_name)
    # Sets the current position of the Buffer to the beginning
    zip_buffer.seek(0)
    # Use this zip_buffer to send it as a return (whenever dowload zip is needed)
    return zip_buffer

# tested


def re_upload(doc):
    sub = str(doc.project_id)
    filename = standardize_accents(doc.filename)
    # current path (.py file is stored in website folder)
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Absolute path outside current path(website) -> current path - 1
    outside_website = os.path.dirname(current_path)
    # path to the folder
    folder_outside = os.path.join(outside_website, PROJECT_FILES_FOLDER)
    # path to the subfolder
    subfolder_path = os.path.join(folder_outside, sub)
    # build entire file path
    file_path = os.path.join(subfolder_path, filename)
    # remove file
    os.remove(file_path)
    # return file_path and use it to save the file in that path
    return file_path
