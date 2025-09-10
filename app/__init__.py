from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
db=SQLAlchemy()
bcrypt=Bcrypt()
socketio = SocketIO(async_mode='eventlet')


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///auction.db'
    app.config['SECRET_KEY']='jkdjskjaghiug345h3uhjqg513hb56'
    socketio.init_app(app)
    db.init_app(app)
    from .main.routes import main
    from .buyers.routes import buyers
    from .sellers.routes import sellers
    from .bids.routes import bids



    app.register_blueprint(main)
    app.register_blueprint(buyers)
    app.register_blueprint(sellers)
    app.register_blueprint(bids)
    return app

