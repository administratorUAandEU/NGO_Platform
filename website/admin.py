import os
import json, uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, Project, News, NewsTag, NewsTaggingTable, ProjectEN, NewsEN, NewsTagEN, NewsTaggingTableEN

admin = Blueprint("admin", __name__)

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

NUMBER_FILE_PATH = "website/static/resources/number_info.json"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@admin.route("/<lang>/administrator", methods=["GET", "POST"])
def load_admin_menu(lang):
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
    return render_template('admin_menu.html', target=target, lang=lang)

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
@admin.route("/<lang>/administrator/manage_projects", methods=["GET", "POST"])
def manage_projects(lang):
    ProjectModel = ProjectEN if lang == "en" else Project
    projects = ProjectModel.query.all()
    return render_template("manage_projects.html", projects=projects, lang=lang)


@admin.route("/<lang>/administrator/delete_project/<int:project_id>", methods=["POST"])
def delete_project(lang, project_id):
    ProjectModel = ProjectEN if lang == "en" else Project
    project = ProjectModel.query.get(project_id)

    if not project:
        flash("Project not found.", category="error")
        return redirect(url_for("admin.manage_projects", lang=lang))

    path = os.path.join(UPLOAD_FOLDER, project.image_path) if project.image_path else None

    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            flash(f"Failed to delete project image: {e}", category="error")

    db.session.delete(project)
    db.session.commit()
    flash("Project and its image deleted successfully.", category="success")
    return redirect(url_for("admin.manage_projects", lang=lang))


@admin.route("/<lang>/administrator/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(lang, project_id):
    ProjectModel = ProjectEN if lang == "en" else Project
    project = ProjectModel.query.get(project_id)

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

            image_path = os.path.join(UPLOAD_FOLDER, name := f"p{lang}{project.id}{get_file_extension(image_file)}")
            image_file.save(image_path)
            project.image_path = name

        db.session.commit()
        flash("Project updated successfully.", category="success")
        return redirect(url_for("admin.manage_projects", lang=lang))

    return render_template("edit_project.html", project=project, lang=lang)


# Manage News
@admin.route("/<lang>/administrator/manage_news", methods=["GET", "POST"])
def manage_news(lang):
    NewsModel = NewsEN if lang == "en" else News
    news_list = NewsModel.query.all()
    return render_template("manage_news.html", news_list=news_list, lang=lang)


@admin.route("/<lang>/administrator/delete_news/<int:news_id>", methods=["POST"])
def delete_news(lang, news_id):
    NewsModel = NewsEN if lang == "en" else News
    NewsTaggingModel = NewsTaggingTableEN if lang == "en" else NewsTaggingTable
    news = NewsModel.query.get(news_id)

    if not news:
        flash("News not found.", category="error")
        return redirect(url_for("admin.manage_news", lang=lang))

    path = os.path.join(UPLOAD_FOLDER, news.image_path) if news.image_path else None

    if path and os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            flash(f"Failed to delete news image: {e}", category="error")

    NewsTaggingModel.query.filter_by(news_id=news_id).delete()

    db.session.delete(news)
    db.session.commit()
    flash("News, its image, and tag associations deleted successfully.",
          category="success")
    return redirect(url_for("admin.manage_news", lang=lang))


@admin.route("/<lang>/administrator/edit_news/<int:news_id>", methods=["GET", "POST"])
def edit_news(lang, news_id):
    NewsModel = NewsEN if lang == "en" else News
    NewsTagModel = NewsTagEN if lang == "en" else NewsTag
    news = NewsModel.query.get(news_id)
    tags = NewsTagModel.query.all()

    if not news:
        flash("News not found.", category="error")
        return redirect(url_for("admin.manage_news", lang=lang))

    if request.method == "POST":
        news.name = request.form.get("name")
        news.location = request.form.get("location")
        news.description = request.form.get("description")
        news.link = request.form.get("link")

        selected_tags = request.form.getlist("tags")
        news.tags = [NewsTagModel.query.get(tag_id) for tag_id in selected_tags]

        image_file = request.files.get("image")
        if image_file:
            if news.image_path:
                delete_file_from_uploads(news.image_path)

            image_path = os.path.join(UPLOAD_FOLDER,name := f"n{lang}{news.id}{get_file_extension(image_file)}")
            image_file.save(image_path)
            news.image_path = name

        db.session.commit()
        flash("News updated successfully.", category="success")
        return redirect(url_for("admin.manage_news", lang=lang))

    return render_template("edit_news.html", news=news, tags=tags, lang=lang)


# Manage NewsTags
@admin.route("/<lang>/administrator/manage_tags", methods=["GET", "POST"])
def manage_tags(lang):
    NewsTagModel = NewsTagEN if lang == "en" else NewsTag
    tags = NewsTagModel.query.all()
    return render_template("manage_tags.html", tags=tags, lang=lang)


@admin.route("/<lang>/administrator/delete_tag/<int:tag_id>", methods=["POST"])
def delete_tag(lang, tag_id):
    NewsTagModel = NewsTagEN if lang == "en" else NewsTag
    NewsTaggingModel = NewsTaggingTableEN if lang == "en" else NewsTaggingTable
    tag = NewsTagModel.query.get(tag_id)
    if not tag:
        flash("Tag not found.", category="error")
        return redirect(url_for("admin.manage_tags", lang=lang))

    NewsTaggingModel.query.filter_by(tag_id=tag_id).delete()

    db.session.delete(tag)
    db.session.commit()
    flash("Tag and its news association deleted successfully.", category="success")
    return redirect(url_for("admin.manage_tags", lang=lang))


@admin.route("/<lang>/administrator/edit_tag/<int:tag_id>", methods=["GET", "POST"])
def edit_tag(lang, tag_id):
    NewsTagModel = NewsTagEN if lang == "en" else NewsTag
    tag = NewsTagModel.query.get(tag_id)
    if request.method == "POST":
        tag.name = request.form.get("name")
        db.session.commit()
        flash("Tag updated successfully.", category="success")
        return redirect(url_for("admin.manage_tags", lang=lang))
    return render_template("edit_tag.html", tag=tag, lang=lang)


@admin.route("/<lang>/administrator/add_tag", methods=["GET", "POST"])
def add_tag(lang):
    if request.method == "POST":
        tag_name = request.form.get("name")
        if not tag_name:
            flash("Tag name cannot be empty.", category="error")
            return redirect(url_for("admin.add_tag", lang=lang))
        NewsTagModel = NewsTagEN if lang == "en" else NewsTag
        existing_tag = NewsTagModel.query.filter_by(name=tag_name).first()
        if existing_tag:
            flash("Tag already exists.", category="error")
            return redirect(url_for("admin.add_tag", lang=lang))

        new_tag = NewsTagModel(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        flash("Tag added successfully.", category="success")
        return redirect(url_for("admin.manage_tags", lang=lang))

    return render_template("create_tag.html", lang=lang)

# Utils
@admin.route("/upload_image", methods=["POST"])
def upload_image():
    if "upload" not in request.files:
        return jsonify({"error": {"message": "No file uploaded"}}), 400

    file = request.files["upload"]

    if file.filename == "":
        return jsonify({"error": {"message": "No selected file"}}), 400

    if file and allowed_file(file.filename):
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)

        file_url = url_for("static", filename=f"uploads/{unique_filename}", _external=True)

        return jsonify({
            "uploaded": True,
            "url": file_url
        }), 200

    return jsonify({"error": {"message": "Invalid file type"}}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
