from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for

from website.utils import get_evaluation_interval_by_id
from .models import Evaluation_Interval, User, Researcher, Evaluator, Project

from . import db


evaluation_interval = Blueprint('evaluation_interval', __name__)


@evaluation_interval.route('/',  methods=['GET', 'POST'])
def evaluation_interval_page():
    # print(datetime.date(datetime.now())) #prints 2023-07-26

    if request.method == 'POST':
        # get ev. interval's data from the form
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # create ev. interval in DB
        new_evaluation_interval = Evaluation_Interval(
            start=datetime.strptime(start_date, '%d/%m/%Y'), end=datetime.strptime(end_date, '%d/%m/%Y'))
        db.session.add(new_evaluation_interval)
        db.session.commit()

    interval_list = Evaluation_Interval.query.filter_by().order_by(
        Evaluation_Interval.end.desc()).all()
    # always return evaluation_interval list
    return render_template('create_evaluation_interval.html', evaluation_intervals=interval_list)
