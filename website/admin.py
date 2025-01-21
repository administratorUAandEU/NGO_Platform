import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, Project, News, NewsTag, NewsTaggingTable

admin = Blueprint("admin", __name__)

UPLOAD_FOLDER = 'website/static/uploads'
NUMBER_FILE_PATH = "website/static/resources/number_info.json"

@admin.route("/administrator", methods=["GET", "POST"])
def load_admin_menu():
    try:
        with open(NUMBER_FILE_PATH, "r", encoding='utf-8') as file:
            data = json.load(file)

        target = data.get("target", 1000)

    except FileNotFoundError:
        target = 10
        print("\nJSON file not found. Using default value.\n")
    except json.JSONDecodeError:
        target = 10
        print("\nInvalid JSON format. Using default value.\n")
    return render_template('admin_menu.html', target=target)

@admin.route("/administrator/update_number", methods=["POST"])
def update_number():
    data = request.get_json()
    new_number = data.get("number")

    if new_number is None:
        return jsonify({"error": "Number is required"}), 400

    try:
        with open(NUMBER_FILE_PATH, "r") as file:
            config = json.load(file)

        config["target"] = new_number

        with open(NUMBER_FILE_PATH, "w") as file:
            json.dump(config, file)

        return jsonify({"success": True, "new_number": new_number}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Manage Projects
@admin.route("/administrator/manage_projects", methods=["GET", "POST"])
def manage_projects():
    projects = Project.query.all()
    return render_template("manage_projects.html", projects=projects)


@admin.route("/administrator/delete_project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        flash("Project not found.", category="error")
        return redirect(url_for("admin.manage_projects"))

    path = os.path.join(UPLOAD_FOLDER, project.image_path) if project.image_path else None

    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            flash(f"Failed to delete project image: {e}", category="error")

    db.session.delete(project)
    db.session.commit()
    flash("Project and its image deleted successfully.", category="success")
    return redirect(url_for("admin.manage_projects"))


@admin.route("/administrator/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        flash("Project not found.", category="error")
        return redirect(url_for("admin.manage_projects"))

    if request.method == "POST":
        project.name = request.form.get("name")
        project.location = request.form.get("location")
        project.description = request.form.get("description")
        project.link = request.form.get("link")
        project.finished = request.form.get("finished") == 'on'

        image_file = request.files.get("image")
        if image_file:
            if project.image_path:
                delete_file_from_uploads(project.image_path)

            image_path = os.path.join(UPLOAD_FOLDER, f"p{project.id}{get_file_extension(image_file)}")
            image_file.save(image_path)

        db.session.commit()
        flash("Project updated successfully.", category="success")
        return redirect(url_for("admin.manage_projects"))

    return render_template("edit_project.html", project=project)


# Manage News
@admin.route("/administrator/manage_news", methods=["GET", "POST"])
def manage_news():
    news_list = News.query.all()
    return render_template("manage_news.html", news_list=news_list)


@admin.route("/administrator/delete_news/<int:news_id>", methods=["POST"])
def delete_news(news_id):
    news = News.query.get(news_id)

    if not news:
        flash("News not found.", category="error")
        return redirect(url_for("admin.manage_news"))

    path = os.path.join(UPLOAD_FOLDER, news.image_path) if news.image_path else None

    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            flash(f"Failed to delete news image: {e}", category="error")

    NewsTaggingTable.query.filter_by(news_id=news_id).delete()

    db.session.delete(news)
    db.session.commit()
    flash("News, its image, and tag associations deleted successfully.",
          category="success")
    return redirect(url_for("admin.manage_news"))


@admin.route("/administrator/edit_news/<int:news_id>", methods=["GET", "POST"])
def edit_news(news_id):
    news = News.query.get(news_id)
    tags = NewsTag.query.all()

    if not news:
        flash("News not found.", category="error")
        return redirect(url_for("admin.manage_news"))

    if request.method == "POST":
        news.name = request.form.get("name")
        news.location = request.form.get("location")
        news.description = request.form.get("description")
        news.link = request.form.get("link")

        selected_tags = request.form.getlist("tags")
        news.tags = [NewsTag.query.get(tag_id) for tag_id in selected_tags]

        image_file = request.files.get("image")
        if image_file:
            if news.image_path:
                delete_file_from_uploads(news.image_path)

            image_path = os.path.join(UPLOAD_FOLDER, f"n{news.id}{get_file_extension(image_file)}")
            image_file.save(image_path)

        db.session.commit()
        flash("News updated successfully.", category="success")
        return redirect(url_for("admin.manage_news"))

    return render_template("edit_news.html", news=news, tags=tags)


# Manage NewsTags
@admin.route("/administrator/manage_tags", methods=["GET", "POST"])
def manage_tags():
    tags = NewsTag.query.all()
    return render_template("manage_tags.html", tags=tags)


@admin.route("/administrator/delete_tag/<int:tag_id>", methods=["POST"])
def delete_tag(tag_id):
    tag = NewsTag.query.get(tag_id)
    if not tag:
        flash("Tag not found.", category="error")
        return redirect(url_for("admin.manage_tags"))

    NewsTaggingTable.query.filter_by(tag_id=tag_id).delete()

    db.session.delete(tag)
    db.session.commit()
    flash("Tag and its news association deleted successfully.", category="success")
    return redirect(url_for("admin.manage_tags"))


@admin.route("/administrator/edit_tag/<int:tag_id>", methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = NewsTag.query.get(tag_id)
    if request.method == "POST":
        tag.name = request.form.get("name")
        db.session.commit()
        flash("Tag updated successfully.", category="success")
        return redirect(url_for("admin.manage_tags"))
    return render_template("edit_tag.html", tag=tag)


@admin.route("/administrator/add_tag", methods=["GET", "POST"])
def add_tag():
    if request.method == "POST":
        tag_name = request.form.get("name")
        if not tag_name:
            flash("Tag name cannot be empty.", category="error")
            return redirect(url_for("admin.add_tag"))

        existing_tag = NewsTag.query.filter_by(name=tag_name).first()
        if existing_tag:
            flash("Tag already exists.", category="error")
            return redirect(url_for("admin.add_tag"))

        new_tag = NewsTag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        flash("Tag added successfully.", category="success")
        return redirect(url_for("admin.manage_tags"))

    return render_template("create_tag.html")

# Utils
def save_file_to_uploads(file, filename):
    '''
    Shortcut to save file to uploads.
    '''
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(image_path)

def get_file_extension(file):
    '''
    Shortcut to get file extension.
    '''
    return os.path.splitext(file.filename)[1] if file else None

def delete_file_from_uploads(filename):
    '''
    Shortcut to delete file from uploads.
    '''
    path = os.path.join(UPLOAD_FOLDER, filename) if filename else None
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            flash(f"Failed to delete file: {e}", category="error")
