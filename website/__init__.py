# Import necessary modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize the SQLAlchemy database object
db = SQLAlchemy()

# Set the name of the SQLite database file
DB_NAME = "database.db"

# Function to create and configure the Flask app
def create_app():
    # Create the Flask app
    app = Flask(__name__)
    
    # Set the secret key for the app (used for session security)
    app.config['SECRET_KEY'] = 'This is my new key'
    
    # Set the URI for the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the database with the Flask app
    db.init_app(app)

    # Import the views and auth blueprints (routes) for the app
    from .views import views
    from .auth import auth

    # Register the blueprints with the app and define their URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the Influencer and Business models
    from .models import Influencer, Business
    
    # Create the database tables using the models
    with app.app_context():
        db.create_all()

    # Initialize the LoginManager for handling user authentication
    login_manager = LoginManager()
    
    # Set the login view for authentication (used for redirects)
    login_manager.login_view = 'auth.login_i'
    login_manager.init_app(app)

    # Define the user loaders for the LoginManager to retrieve user objects
    @login_manager.user_loader
    def load_Influencer(id):
        return Influencer.query.get(int(id))
    
    @login_manager.user_loader
    def load_Business(id):
        return Business.query.get(int(id))

    # Return the configured Flask app
    return app


# Function to create the database (if it does not exist)
def create_database(app):
    # Check if the database file does not exist
    if not path.exists('website/' + DB_NAME):
        # Create all the database tables using the app context
        db.create_all(app=app)
        print('Created Database!')
