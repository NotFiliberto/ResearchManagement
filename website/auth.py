from flask import Blueprint, render_template, request

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
        # TODO validation logic
        # TODO register logic
        data = request.form
        print(data)
        return "registra utente"

    return render_template('auth/signup.html', text="ADDITIONAL TEXT", boolean=False)
