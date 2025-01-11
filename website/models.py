'''
Database scheme
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    '''
    Projects table.
    '''
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    description = db.Column(db.String)
    link = db.Column(db.String)
    image_path = db.Column(db.String, nullable=True)
    finished = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Project {self.name}>"

class News(db.Model):
    '''
    News table.
    '''
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    link = db.Column(db.String, nullable=True)

    tags = db.relationship('NewsTag', secondary='news_tagging_table', backref='news', lazy='dynamic')

class NewsTag(db.Model):
    '''
    Hashtags for news.
    '''
    __tablename__ = 'news_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<NewsTag {self.name}>"

class NewsTaggingTable(db.Model):
    '''
    Helper table for assigning tags to news and vice versa.
    '''
    __tablename__ = 'news_tagging_table'

    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('news_tags.id'), primary_key=True)
