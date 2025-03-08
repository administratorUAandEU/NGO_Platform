'''
Perform search in news and projects
by location, description, and name.
'''
from flask import Blueprint, render_template, request
from .models import News, Project, NewsEN, ProjectEN

search = Blueprint("search", __name__)

@search.route("/<lang>/search", methods=["GET"])
def search_page(lang):
    '''
    Route for search page with language support.
    '''
    if lang not in ["en", "ua"]:
        lang = "ua"

    results = {"news": [], "projects": []}
    query = request.args.get("query", "").strip()

    NewsModel = NewsEN if lang == "en" else News
    ProjectModel = ProjectEN if lang == "en" else Project

    if query:
        news_results = NewsModel.query.filter(
            (NewsModel.name.ilike(f"%{query}%")) | 
            (NewsModel.description.ilike(f"%{query}%")) | 
            (NewsModel.location.ilike(f"%{query}%"))
        ).all()
        results["news"] = news_results

        project_results = ProjectModel.query.filter(
            (ProjectModel.name.ilike(f"%{query}%")) | 
            (ProjectModel.description.ilike(f"%{query}%")) | 
            (ProjectModel.location.ilike(f"%{query}%"))
        ).all()
        results["projects"] = project_results
    else:
        results["news"] = NewsModel.query.all()
        results["projects"] = ProjectModel.query.all()

    return render_template("search.html", query=query, results=results, lang=lang)
