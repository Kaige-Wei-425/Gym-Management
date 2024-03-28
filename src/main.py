import os
from flask import Flask
# Import library objects from init.py
from init import db, ma, bcrypt, jwt

# Function to create the flask app
def create_app():
    app = Flask(__name__)

    # Configurations
    #                                         dbms   + driver     db_user: password   URL: port  db_name
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    
    # Connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register the blue print to the falsk app
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    
    # Return the instance of the app
    return app