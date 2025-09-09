from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db=SQLAlchemy()
bcrypt=Bcrypt()



def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///auction.db'
    app.config['SECRET_KEY']='jkdjskjaghiug345h3uhjqg513hb56'
    db.init_app(app)
    from .main.routes import main
    from .buyers.routes import buyers
    from .sellers.routes import sellers

    app.register_blueprint(main)
    app.register_blueprint(buyers)
    app.register_blueprint(sellers)
    return app

