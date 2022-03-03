import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .models import db
from src.users.routes import bcrypt
from src.models import login_manager
from src.users.utils import mail

#Application Factory Function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    migrate = Migrate()
  
    
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
       app.config.from_mapping(
        SECRET_KEY= os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DB_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
     
    )
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    from src.posts.routes import posts
    from src.users.routes import users
    from src.main.routes import main
    from src.errors.errorhandlers import errors   
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.static_folder = 'static'
    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    Marshmallow(app)
    db.create_all()

   
    
    return app

