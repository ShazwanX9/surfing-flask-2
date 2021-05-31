from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import time

from .config import ConstData
from os import path, stat

###########################################################################################

db = SQLAlchemy()

def create_database(app, filepath="./"):
    """Check Existance of Database File"""

    if not path.exists(filepath + str(ConstData.DB_NAME)):
        db.create_all(app=app)
        print("New Database Created!")

def create_app():
    """Application Core"""

    app = Flask(__name__)
    app.config.from_object(ConstData.CONFIG_FILEPATH)

    with app.app_context():
        # Init Database
        db.init_app(app)

        # Imports
        from .dbmanip import User, Feed, Chat
        from .auth import auth
        from .view import view

        # Connect To Database
        create_database(app=app)

        # Register Routes Blueprint
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(view, url_prefix='/')

        # Register Context Processor
        @app.context_processor
        def override_url_for():
            return dict(url_for=dated_url_for)

        def dated_url_for(endpoint, **values):
            if endpoint == 'static':
                filename = values.get('filename', None)
                if filename:
                    file_path = path.join(app.root_path,
                                        endpoint, filename)
                    values['q'] = int(stat(file_path).st_mtime)
            return url_for(endpoint, **values)
        
        # Login Manager
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login_phase'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get( int(id) )

        return app

class Setup():
    # SETUP
    app = create_app()
    socketio = SocketIO(app)  # used for user communication

    # Communication Function
    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')

    @socketio.on('my event')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        socketio.emit('my response', json, callback=messageReceived)