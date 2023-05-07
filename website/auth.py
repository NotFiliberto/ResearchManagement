from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/signin')
def sign_in():
    return render_template('auth/signin.html', text="ADDITIONAL TEXT", boolean=False)


@auth.route('/signout')
def sign_out():
    return "<div>logout page</div>"


@auth.route('/signup')
def sign_up():
    return render_template('auth/signup.html', text="ADDITIONAL TEXT", boolean=False)
