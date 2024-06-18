from flask import Flask
from os import path
from flask_login import LoginManager
from applications.db import db
from flask_restful import Api
from flask_mail import *





DB_Name = 'ticketbookingappdb.sqlite3'

def Create_ticketbookingapplicaton():

    app=Flask(__name__ ,template_folder='templates')
    api=Api(app)

    app.app_context().push()
    app.config['SECRET_KEY'] = "secretkeepitsecret"


    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_Name}'
    db.init_app(app)


    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='mycirclebloglite@gmail.com'
    app.config['MAIL_PASSWORD']='afppoeqwbfuvebuc'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True


    from applications.models import User,Venue,Show,Venue_show,Review,Booking,Capacity

    Create_DB(app)


    from applications.admin_controlls import admin_controll_routes
    from applications.admin_auth import admin_auth_routes
    from applications.user_controlls import user_controll_routes
    from applications.user_auth import user_auth_routes

    app.register_blueprint(admin_controll_routes,url_prefix="/")

    app.register_blueprint(admin_auth_routes,url_prefix="/")

    app.register_blueprint(user_controll_routes,url_prefix="/")

    app.register_blueprint(user_auth_routes,url_prefix="/")



    login_manager=LoginManager()
    login_manager.login_view="user_auth_routes.user_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))





    return app,api


    




def Create_DB(app):
    if not path.exists("instance/" + DB_Name ):
        with app.app_context():
            db.create_all()
        print("Database has been created!")

