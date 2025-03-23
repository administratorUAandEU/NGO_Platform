from flask import Blueprint, render_template
from .models import Config

about_us = Blueprint("about_us", __name__)
NUMBER_FILE_PATH = "website/static/resources/number_info.json"

@about_us.route("/<lang>/about_us", methods=["GET", "POST"])
def load_about_us(lang='ua'):
    try:
        config = Config.query.first()

        if config:
            target = config.target
            duration = config.duration
        else:
            target = 1000
            duration = 3000

    except Exception as e:
        target = 1000
        duration = 3000
        print("\nError fetching config data from database. Using default values.\n")

    return render_template('aboutus.html', target=target, duration=duration, lang=lang)
