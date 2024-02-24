from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

from .events import socketio
from .updater import updateThread


print("Creating auth database...")
db = SQLAlchemy()

def create_app():
    print("Creating flask app...")
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret!" # Please for the love of christ change before production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    print("Starting updateThread...")
    thread = updateThread()
    thread.start()

    print("Starting authentication routes...")
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    print("Starting main routes...")
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    print("Initalizting SocketIO...")
    socketio.init_app(app)

    with app.app_context():
        db.create_all()
        
    return app
