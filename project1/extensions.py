
#Creating the SQLAlchemy extension that can be imported all over our app as needed 
#initialize sqlalchemy so it can setup everything it needs    
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
