from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# Initialize Flask app


def create_app():
    app = Flask(__name__)
    # Encrypt cookie data for session
    app.config['SECRET_KEY'] = 'josiefnapwpawoj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize DB
    db.init_app(app)

    # Import views
    from .views import views
    from .auth import auth

    # Register views with empty prefixes
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import models
    from .models import User

    # Create database (if not exists)
    create_database(app)

    login_manager = LoginManager()
    # Set location to redirect user if not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
