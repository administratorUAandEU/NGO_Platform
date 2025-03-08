from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory, redirect, url_for, abort
from flask_login import login_required, current_user, AnonymousUserMixin
from werkzeug.exceptions import HTTPException

home = Blueprint("home", __name__)

@home.route("/", methods=["GET", "POST"])
@home.route("/<lang>/home", methods=["GET", "POST"])
def load_home(lang="ua"):
    if lang not in ["en", "ua"]:
        abort(404)
    return redirect(url_for('about_us.load_about_us', lang=lang))

@home.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('../uploads', filename)

@home.route('/redirect/<path:hrefed>')
def redirect_to(hrefed):
    return redirect(hrefed)
