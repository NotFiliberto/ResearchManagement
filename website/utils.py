from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

utils = Blueprint('utils', __name__)

