import os
from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory, redirect, url_for
from .models import db, News, NewsTag, NewsTaggingTable
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


news = Blueprint("news", __name__)


@news.route("/news", methods=["GET", "POST"])
def load_news():
    news_articles = News.query.all()
    news_data = []

    for article in news_articles:
        image_filename = article.image_path
        image_path = os.path.join("website", "static", "uploads", image_filename) if image_filename else 'NaN'
        news_data.append({
            "id": article.id,
            "name": article.name,
            "location": article.location,
            "date": article.date,
            "description": article.description,
            "link": article.link,
            "image_exists": os.path.exists(image_path),
            "image_path": f"uploads/{image_filename}" if os.path.exists(image_path) else None,
            "tags": [tag.name for tag in article.tags]
        })

    return render_template('news.html', news_articles=news_data)

@news.route("/news/new", methods=["GET", "POST"])
def create_news():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        description = request.form.get("description")
        link = request.form.get("link")
        tag_names = request.form.getlist("tags")

        if not name or not location or not description:
            flash("Name, location, and description are required.", category="error")
            return redirect(url_for("news.create_news"))

        news_date = datetime.today().date()

        new_news = News(
            name=name,
            location=location,
            description=description,
            link=link if link else None,
            date=news_date
        )

        db.session.add(new_news)

        for tag_name in tag_names:
            tag = NewsTag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = NewsTag(name=tag_name)
                db.session.add(tag)
            new_news.tags.append(tag)

        try:
            db.session.commit()

            image_path = None
            if 'image' in request.files:
                image = request.files['image']
                if image and allowed_file(image.filename):
                    file_extension = image.filename.rsplit('.', 1)[1].lower()
                    filename = secure_filename(
                        f"n{new_news.id}.{file_extension}")
                    image_path = os.path.join(
                        'website', 'static', 'uploads', filename)
                    image.save(image_path)

                    new_news.image_path = f"{filename}"
                    db.session.commit()

            flash("News article created successfully!", category="success")
            return redirect(url_for('admin.manage_news'))
        except IntegrityError:
            db.session.rollback()
            flash("Error creating news article.", category="error")
            return redirect(url_for("news.create_news"))

    tags = NewsTag.query.all()
    return render_template("create_news.html", tags=tags)
