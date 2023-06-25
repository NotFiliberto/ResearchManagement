from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from website.models import Project, ProjectStatus
from .utils import get_project, restrict_user


document = Blueprint('document', __name__)


@document.route('/download',  methods=['GET', 'POST'])
@login_required
def download():
    document_id = request.args.get('document_id')
