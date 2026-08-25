from flask import Flask
from pydantic import ValidationError
from flaskr.extensions import db
from flask_migrate import Migrate
import os

migrate = Migrate()

#creating and configuring flask app. Uses the factory pattern to create and return a new Flask app
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]  
    db.init_app(app) 
   # Migrate.init_app(app, db)  
    # if test_config is None: 
    #     app.config.from_pyfile('config.py', silent =True)
    # else:
    #     app.config.from_mapping(test_config)

    #os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/hello')
    def hello():
        return "hello world"
    return app 
        