'''
Database scheme
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config(db.Model):
    '''
    Configuration data for target and duration.
    '''
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.Integer, nullable=False, default=1000)
    duration = db.Column(db.Integer, nullable=False, default=3000)

    def __repr__(self):
        return f"<Config target={self.target} duration={self.duration}>"

# UA
class Project(db.Model):
    '''
    Projects table.
    '''
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
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
    description = db.Column(db.Text(), nullable=False)
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

#EN
class ProjectEN(db.Model):
    '''
    Projects table.
    '''
    __tablename__ = 'projects_en'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.String)
    image_path = db.Column(db.String, nullable=True)
    finished = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Project_en {self.name}>"

class NewsEN(db.Model):
    '''
    News table.
    '''
    __tablename__ = 'news_en'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image_path = db.Column(db.String, nullable=True)
    link = db.Column(db.String, nullable=True)

    tags = db.relationship('NewsTagEN', secondary='news_tagging_table_en', backref='news_en', lazy='dynamic')

class NewsTagEN(db.Model):
    '''
    Hashtags for news.
    '''
    __tablename__ = 'news_tags_en'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<NewsTagEn {self.name}>"

class NewsTaggingTableEN(db.Model):
    '''
    Helper table for assigning tags to news and vice versa.
    '''
    __tablename__ = 'news_tagging_table_en'

    news_id = db.Column(db.Integer, db.ForeignKey('news_en.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('news_tags_en.id'), primary_key=True)
