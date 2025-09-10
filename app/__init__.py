from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_login import LoginManager
db=SQLAlchemy()
bcrypt=Bcrypt()
socketio = SocketIO(async_mode='eventlet')

login_manager=LoginManager()
login_manager.login_view='buyers.login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    from app.models import Buyers 
    try:
        return Buyers.query.get(int(user_id))
    except (ValueError, TypeError):
        return None


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///auction.db'
    app.config['SECRET_KEY']='jkdjskjaghiug345h3uhjqg513hb56'
    socketio.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .main.routes import main
    from .buyers.routes import buyers
    from .sellers.routes import sellers
    from .bids.routes import bids



    app.register_blueprint(main)
    app.register_blueprint(buyers)
    app.register_blueprint(sellers)
    app.register_blueprint(bids)
    return app

