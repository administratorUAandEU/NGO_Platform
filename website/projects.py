import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from .models import db, Project

projects = Blueprint("projects", __name__)

UPLOAD_FOLDER = 'website/static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@projects.route("/projects", methods=["GET"])
def load_projects():
    _projects = Project.query.all()
    project_data = []

    for project in _projects:
        image_filename = project.image_path
        image_path = os.path.join(
            "website", "static", "uploads", image_filename if image_filename else 'NaN')
        project_data.append({
            "id": project.id,
            "name": project.name,
            "location": project.location,
            "description": project.description,
            "link": project.link,
            "image_exists": os.path.exists(image_path),
            "image_path": f"uploads/{image_filename}" if os.path.exists(image_path) else None,
            "finished": project.finished
        })

    return render_template("projects.html", projects=project_data)


@projects.route("/projects/new", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        project_name = request.form.get("name")
        project_location = request.form.get("location")
        project_description = request.form.get("description")
        project_link = request.form.get("link")
        image = request.files.get("image")

        if not project_name or not project_location or not project_description:
            flash("All fields except 'Link' are required.", category="error")
            return redirect(url_for("projects.create_project"))

        new_project = Project(
            name=project_name,
            location=project_location,
            description=project_description,
            link=project_link if project_link else None,
        )
        db.session.add(new_project)
        db.session.commit()

        image_filename = None
        if image and allowed_file(image.filename):
            file_extension = os.path.splitext(image.filename)[1]
            image_filename = f"p{new_project.id}{file_extension}"

            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)

            new_project.image_path = image_filename
            db.session.commit()

        flash("Project created successfully!", category="success")
        return redirect(url_for('admin.manage_projects'))

    return render_template("create_project.html")


@projects.route("/projects/<int:project_id>", methods=["GET"])
def view_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        abort(404)

    image_path = project.image_path
    project_data = {
        "id": project.id,
        "name": project.name,
        "location": project.location,
        "description": project.description,
        "link": project.link,
        "image_exists": os.path.exists(os.path.join(UPLOAD_FOLDER, image_path)) if image_path else False,
        "image_path": f"uploads/{image_path}" if image_path else None,
        "finished": project.finished
    }

    return render_template("project_detail.html", project=project_data)
