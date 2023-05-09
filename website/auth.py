from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/signin')
def sign_in():
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

        if (len(username) <= 2):
            flash('Username must be grater than 2 characters',
                  category='input_error')
        else:
            flash('Account created', category='success')

        # TODO registration logic (db)
        # return "registra utente"

    return render_template('auth/signup.html', text="ADDITIONAL TEXT", boolean=False)
