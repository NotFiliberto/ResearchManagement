from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # authentication
        user = User.query.filter_by(email=email).first()

        if user:
            # check password
            if check_password_hash(user.password, password):
                flash('Signed in successfully', category='success')
                return redirect(url_for('views.home'))  # redirect after login

            else:
                flash('Wrong email or password!',
                      category='error')
        else:
            flash('Wrong email or password!',
                  category='error')

    return render_template('auth/signin.html', text="ADDITIONAL TEXT", boolean=False)


@auth.route('/signout')
def sign_out():
    return "<div>logout page</div>"


@auth.route('/signup', methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        data = request.form
        print(data)

        # TODO validation logic
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user already exists
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif (len(username) <= 2):
            flash('Username must be grater than 2 characters',
                  category='error')
        else:
            # TODO registration logic (db)
            new_user = User(email=email, username=username,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()  # notify the db that we've made some changes so update it

            flash('Account created', category='success')

            # inherit the url from view (BLUPRINT_NAME.FUNCTION_NAME u want go to)
            return redirect(url_for('views.home'))

        # return "registra utente"

    return render_template('auth/signup.html', text="ADDITIONAL TEXT", boolean=False)
