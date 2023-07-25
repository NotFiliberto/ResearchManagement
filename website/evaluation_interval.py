from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Evaluation_Interval
from .utils import get_evaluation_interval_by_id

from . import db


evaluation_interval = Blueprint('evaluation_interval', __name__)


@evaluation_interval.route('/',  methods=['GET', 'POST'])
def evaluation_interval_page():
    if request.method == 'GET':
        # show all existing intervals -> create a list of intervals
        ev_intervals = Evaluation_Interval.query.all()
        interval_list = []
        print("\n\n\n")
        for ev_interval in ev_intervals:
            interval_list.append(get_evaluation_interval_by_id(ev_interval.evaluation_interval_id))
            print("Interval[", ev_interval.evaluation_interval_id,"]: ", ev_interval.start, ev_interval.end, "\n")

        return render_template('create_evaluation_interval', evaluation_intervals=interval_list)

    if request.method == 'POST':
        # get ev. interval's data from the form 
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        # create ev. interval in DB 
        evaluation_interval = Evaluation_Interval(start=start_date, end=end_date)
        db.session.add(evaluation_interval)
        db.session.commit()

        return render_template('create_evaluation_interval.html')
