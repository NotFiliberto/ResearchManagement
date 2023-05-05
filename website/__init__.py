from flask import Flask


def create_app():
    app = Flask(__name__)  # name of the file

    app.config['SECRET_KEY'] = 'notFil6e660'  # use .env file in production

    # blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
