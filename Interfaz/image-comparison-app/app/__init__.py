from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')  # Ensure the config file is correctly loaded
    app.secret_key = app.config['SECRET_KEY']  # Load SECRET_KEY from the configuration file

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure database tables are created

    from app import routes
    app.register_blueprint(routes.app)  # Ensure the blueprint is registered

    return app