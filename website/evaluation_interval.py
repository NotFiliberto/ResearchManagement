from datetime import datetime
from flask import Blueprint, render_template, request
from .models import Evaluation_Interval

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

    interval_list = Evaluation_Interval.query.order_by(
        Evaluation_Interval.end.desc()).all()

    for interval in interval_list:
        interval.start = interval.start.strftime("%d/%m/%Y")
        interval.end = interval.end.strftime("%d/%m/%Y")
    # always return evaluation_interval list
    return render_template('create_evaluation_interval.html', evaluation_intervals=interval_list)