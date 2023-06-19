from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # essential for managing signed in users

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)  # name of the file

    app.config['SECRET_KEY'] = 'notFil6e660'  # use .env file in production
    # TODO change sqlite with postgressql (look up docs)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)  # init db

    # blueprints
    from .views import views
    from .auth import auth
    from .researcher import researcher
    from .evaluator import evaluator

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(researcher, url_prefix='/researcher')
    app.register_blueprint(evaluator, url_prefix='/evaluator')

    # create db
    from .models import User, Researcher



    with app.app_context():
        db.create_all()




    # setup flask login manager
    login_manager = LoginManager()  # create login manager

    # redirect to this template if the user is not signed in
    login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)

    # tell flask login to use this function to load the user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
