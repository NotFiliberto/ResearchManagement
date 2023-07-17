from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Researcher, Evaluator, Project
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/test', methods=["GET", "POST"])
def test():
    return "hello_world"


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
                flash('Accesso avvenuto con successo', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))

            else:
                flash('Email o password errata!',
                      category='error')
        else:
            flash('Email o password errata!',
                  category='error')

    return render_template('auth/signin.html')


@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.sign_in'))


@auth.route('/signup', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        print(data)

        # TODO validation logic
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        # check if user already exists
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Esiste già un account con questa email', category='error')
        elif (len(username) <= 2):
            flash('Lo username come minimo deve avere 3 caratteri',
                  category='error')
        else:
            # TODO registration logic (db)
            try:
                if (user_type.upper() == "EVALUATOR"):
                    new_user = Evaluator(username=username, email=email, password=generate_password_hash(
                        password, method='scrypt'))
                elif user_type.upper() == "RESEARCHER":
                    new_user = Researcher(username=username, email=email, password=generate_password_hash(
                        password, method='scrypt'))
                else:
                    new_user = None

                if new_user is None:
                    flash("Errore durante la creazione dell'utente!",
                          category="error")
                else:
                    db.session.add(new_user)
                    db.session.commit()  # notify the db that we've made some changes so update it

                    flash('Account creato con successo', category='success')

                    # signin user
                    login_user(remember=True, user=new_user)

                    # inherit the url from view (BLUPRINT_NAME.FUNCTION_NAME u want go to)
                    return redirect(url_for('views.home'))
            except:
                flash('Errore durante la registrazione, riprova!',
                      category='error')

    return render_template('auth/signup.html')
