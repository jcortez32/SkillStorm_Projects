from flask import Flask
from pydantic import ValidationError
from src.extensions import db
from flask_migrate import Migrate
from flask import jsonify
import os
from src.routes import comp_bp
migrate = Migrate()

#creating and configuring flask app. Uses the factory pattern to create and return a new Flask app
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]  
    db.init_app(app) 
    migrate.init_app(app, db)  

    app.register_blueprint(comp_bp)
    @comp_bp.route('/hel')
    def hello():
        return "hello world"
    return app 
        