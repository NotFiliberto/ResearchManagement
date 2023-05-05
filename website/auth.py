from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/signin')
def sign_in():
    return "<div>login page</div>"


@auth.route('/signout')
def sign_out():
    return "<div>logout page</div>"


@auth.route('/signup')
def sign_up():
    return "<div>sign up page</div>"
