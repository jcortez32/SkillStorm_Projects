from flask import Flask
from project1.extensions import db, migrate
#from flask_migrate import Migrate
import os
from project1.Company_Management.routes import company_bp
from project1.Press_Release_Management.routes import press_bp
from project1.Sentiment_Analysis.routes import analysis_bp
from project1.routes import main_bp

#creating and configuring flask app. Uses the factory pattern to create and return a new Flask app
def create_app():
    app = Flask(__name__)

    #main database (ie. companies)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]  
    db.init_app(app) 
    migrate.init_app(app, db)  

    #registering blueprints
    app.register_blueprint(company_bp)
    app.register_blueprint(press_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(main_bp)
    
    return app
