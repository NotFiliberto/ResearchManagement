from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/',  methods=['GET', 'POST'])
@login_required
def home():
<<<<<<< HEAD
    return render_template('home.html', user=current_user)
=======
    return render_template('home.html', user=current_user)
>>>>>>> 9b262272dc9553e341a170a440fa45d30ab7a82c
