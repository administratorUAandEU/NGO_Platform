from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory, redirect, url_for
from flask_login import login_required, current_user, AnonymousUserMixin
from werkzeug.exceptions import HTTPException
# from . import db
# import json

home = Blueprint("home", __name__)

@home.route("/", methods = ["GET","POST"])
@home.route("/home", methods = ["GET","POST"])
def load_home():
    return render_template('index.html')

@home.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('../uploads', filename)

@home.route('/redirect/<path:hrefed>')
def redirect_to(hrefed):
    return redirect(hrefed)