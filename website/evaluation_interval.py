from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Researcher, Evaluator, Project

from . import db


evaluation_interval = Blueprint('evaluation_interval', __name__)


@evaluation_interval.route('/',  methods=['GET', 'POST'])
def evaluation_interval_page():

    return render_template('create_evaluation_interval.html')
