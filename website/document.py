from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required, current_user
from website.models import Document
from website.models import Project, ProjectStatus
from .utils import get_project, restrict_user, download_document


document = Blueprint('document', __name__)


@document.route('/download',  methods=['GET', 'POST'])
@login_required
def download():
    document_id = request.args.get('document_id')
    file_path = download_document(document_id)
    return send_file(file_path, as_attachment=True)