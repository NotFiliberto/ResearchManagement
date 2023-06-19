from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Researcher, Evaluator
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


#TODO route per i projects con def metodi crud: 
#  create(idProgetto, ricercatore), read(ricercatore, valutatore), update, delete  (crud operations)
# sempre controllare che chi fa un'operazione debba essere loggato (prima)
# per fare create -> /root/create : se il metodo è GET reinderizzi sulla pagina createProject.html
# se il metodo è POST (if requested.method == "POST"), returno la stringa che
#  il progetto è stato creato con successo
# tutte  le route sono renderizzate da una cartella apposita fuori da website 
# @auth.route()
@auth.route('/test', methods=["GET", "POST"])
def test():
    return "hello_world"

@auth.route('/signin', methods=["GET", "POST"])
def sign_in():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        #db.session.add(Researcher(username='Vin1', password=generate_password_hash("1234", method='scrypt'), email="Vin1@gmail.com"))
        #db.session.commit()

        #db.session.add(Evaluator(username='Vin2', password=generate_password_hash("1234", method='scrypt'), email="Vin2@gmail.com"))
        #db.session.commit()
        
        print("SEPARATOR")
        print(User.query.filter_by(email="vineet.cesca@gmail.com").first())
        print(Researcher.query.filter_by(id=user.id).all())
        # authentication
        
        users = User.query.all()
        print(user.id)
        print("users here:")
        print(User.query.all())
        for u in users:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 
        
        
        researchers = Researcher.query.all()
        print("researchers here:")
        print(Researcher.query.all())
        for u in researchers:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 

        evaluators = Evaluator.query.all()
        print("evaluators here:")
        print(Evaluator.query.all())
        for u in evaluators:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 

        print("sus")

        if user:
            # check password
            if check_password_hash(user.password, password):
                flash('Signed in successfully', category='success')
                login_user(user, remember=True)
                #TODO redirect condizionato in base al tipo di utente
                #if( user is valutatore ) -> redirect to valutatore page
                #if( user is ricercatore ) -> redirect to ricercatore page
                #Notice, researchers/evaluators must be created first and then
                # check if they are logged as users
                if user.__class__.__name__ == "Researcher":
                    print("user is a researcher")
                    return redirect(url_for('researcher.researcher_home'))
                elif user.__class__.__name__ == "Evaluator":
                    print("user is an evaluator")
                    return redirect(url_for('evaluator.evaluator_home'))
                else:
                    print("user is a classic")
                    return redirect(url_for('views.home'))  # redirect after login
            else:
                flash('Wrong email or password!',
                      category='error')
        else:
            flash('Wrong email or password!',
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
                            password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()  # notify the db that we've made some changes so update it

            flash('Account created', category='success')

            # signin user
            login_user(remember=True, user=new_user)

            # inherit the url from view (BLUPRINT_NAME.FUNCTION_NAME u want go to)
            return redirect(url_for('views.home'))

        # return "registra utente"

    return render_template('auth/signup.html', text="")
