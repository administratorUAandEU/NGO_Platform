'''
Perform search in news and projects
by location, description, and name.
'''
from flask import Blueprint, render_template, request
from .models import News, Project

search = Blueprint("search", __name__)

@search.route("/search", methods=["GET"])
def search_page():
    '''
    Route for search page.
    '''
    query = request.args.get("query", "").strip()
    results = {"news": [], "projects": []}

    if query:
        news_results = News.query.filter(
            (News.name.ilike(f"%{query}%")) | 
            (News.description.ilike(f"%{query}%")) | 
            (News.location.ilike(f"%{query}%"))
        ).all()
        results["news"] = news_results

        project_results = Project.query.filter(
            (Project.name.ilike(f"%{query}%")) | 
            (Project.description.ilike(f"%{query}%")) | 
            (Project.location.ilike(f"%{query}%"))
        ).all()
        results["projects"] = project_results
    else:
        results["news"] = News.query.all()
        results["projects"] = Project.query.all()

    return render_template("search.html", query=query, results=results)
