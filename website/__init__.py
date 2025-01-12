'''
Module for platform.
'''

from datetime import datetime
from os import path
from flask import Flask, url_for, render_template
from . import models

DB_NAME = 'db.db'

def create_app():
    '''
    Flask Web App
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    models.db.init_app(app)

    #error
    @app.errorhandler(500)
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html")

    from .home import home
    from .news import news
    from .about import about_us
    from .projects import projects
    from .admin import admin
    from .search import search

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(news, url_prefix='/')
    app.register_blueprint(about_us, url_prefix='/')
    app.register_blueprint(projects, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(search, url_prefix="/")

    with app.app_context():
        create_database(app)

    return app

def create_database(app):
    '''
    Create a db with basic hashtags.
    '''
    if not path.exists('instance/' + DB_NAME):
        models.db.create_all()
        t1 = models.NewsTag(
            name = 'News'
        )
        t2 = models.NewsTag(
            name = 'Interviews'
        )
        t3 = models.NewsTag(
            name = 'Articles'
        )
        t4 = models.NewsTag(
            name = 'Euro-Atlantic integration'
        )
        t5 = models.NewsTag(
            name = 'Russian-Ukrainian war'
        )
        t6 = models.NewsTag(
            name = 'Regions development'
        )
        t7 = models.NewsTag(
            name = 'Environmental protection'
        )
        models.db.session.add_all([t1,t2,t3,t4,t5,t6,t7])
        models.db.session.commit()
        print('DB created!')
