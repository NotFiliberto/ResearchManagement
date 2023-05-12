from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
