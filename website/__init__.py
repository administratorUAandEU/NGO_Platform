'''
Module for platform.
'''

from os import path
from flask import Flask, session, render_template, request
from flask_migrate import Migrate
from . import models

DB_NAME = 'db.db'

def create_app():
    '''
    Flask Web App
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ngo_platform_user:iiW9ZSNAFhdxdtUBJSRRcPYUk5IovfJZ@dpg-cvfuoqtsvqrc73d4o2f0-a.frankfurt-postgres.render.com/ngo_platform'
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    models.db.init_app(app)
    migrate = Migrate(app, models.db)

    #error
    @app.errorhandler(500)
    @app.errorhandler(404)
    def page_not_found(error):
        lang = error.description if error.description and error.description in ['ua', 'en'] else 'ua'
        return render_template("error.html", lang=lang), error.code

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
    models.db.create_all()
    if not models.NewsTag.query.first():
        NewsTagModel = models.NewsTagEN
        t1 = NewsTagModel(
            name = 'News'
        )
        t2 = NewsTagModel(
            name = 'Interviews'
        )
        t3 = NewsTagModel(
            name = 'Articles'
        )
        t4 = NewsTagModel(
            name = 'Euro-Atlantic integration'
        )
        t5 = NewsTagModel(
            name = 'Russian-Ukrainian war'
        )
        t6 = NewsTagModel(
            name = 'Regions development'
        )
        t7 = NewsTagModel(
            name = 'Environmental protection'
        )
        models.db.session.add_all([t1,t2,t3,t4,t5,t6,t7])
        NewsTagModel = models.NewsTag
        t1 = NewsTagModel(
            name = 'Новини'
        )
        t2 = NewsTagModel(
            name = 'Інтерв\'ю'
        )
        t3 = NewsTagModel(
            name = 'Заголовки'
        )
        t4 = NewsTagModel(
            name = 'Євро-Атлантична інтеграція'
        )
        t5 = NewsTagModel(
            name = 'Російсько-Українська війна'
        )
        t6 = NewsTagModel(
            name = 'Розвиток регіонів'
        )
        t7 = NewsTagModel(
            name = 'Захист Довкілля'
        )
        models.db.session.add_all([t1,t2,t3,t4,t5,t6,t7])
        models.db.session.commit()
        print('DB created!')
