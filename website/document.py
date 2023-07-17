from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required, current_user
from website.models import Document
from website.models import Project
from .utils import download_document, download_zip_documents, get_project, restrict_user


document = Blueprint('document', __name__)


@document.route('/download',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, ['Researcher', 'Evaluator'])
def download():
    document_id = request.args.get('document_id')
    file_path = download_document(document_id)
    return send_file(file_path, as_attachment=True)

@document.route('/downloadzip',  methods=['GET', 'POST'])
@login_required
@restrict_user(current_user, ['Researcher', 'Evaluator'])
def downloadzip():
    project_id = request.args.get('project_id')
    # project_id = 1
    project = Project.query.filter_by(project_id=project_id).first()
    if project_id is None or project is None:
        return redirect(url_for('static', filename='404.html'))
    zip_buffer = download_zip_documents(project_id)
    name = 'project_{}_files.zip'.format(project_id)
    return send_file(zip_buffer, as_attachment=True, download_name=name)