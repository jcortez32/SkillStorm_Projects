from flask import Flask
from src.extensions import db, migrate
#from flask_migrate import Migrate
import os
from src.routes import main_bp

#creating and configuring flask app. Uses the factory pattern to create and return a new Flask app
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]  
    db.init_app(app) 
    migrate.init_app(app, db)  

    #registering blueprints
    app.register_blueprint(main_bp)
    return app 
        