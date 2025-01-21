from flask import Blueprint, render_template
import json

about_us = Blueprint("about_us", __name__)
NUMBER_FILE_PATH = "website/static/resources/number_info.json"

@about_us.route("/about_us", methods=["GET", "POST"])
def load_about_us():
    try:
        with open(NUMBER_FILE_PATH, "r", encoding='utf-8') as file:
            data = json.load(file)

        target = data.get("target", 1000)
        duration = data.get("duration", 3000)

    except FileNotFoundError:
        target = 10
        duration = 2000
        print("\nJSON file not found. Using default values.\n")
    except json.JSONDecodeError:
        target = 10
        duration = 2000
        print("\nInvalid JSON format. Using default values.\n")

    return render_template('aboutus.html', target=target, duration=duration)
