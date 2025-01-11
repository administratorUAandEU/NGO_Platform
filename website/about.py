from flask import Blueprint, render_template, request, flash, jsonify, send_from_directory, redirect, url_for
from flask_login import login_required, current_user, AnonymousUserMixin
from werkzeug.exceptions import HTTPException
# from . import db
# import json

about_us = Blueprint("about_us", __name__)

@about_us.route("/about_us", methods = ["GET","POST"])
def load_about_us():
    return render_template('aboutus.html')