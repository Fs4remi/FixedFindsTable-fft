from app import app
from app.scraper import scrape

from flask import render_template, request, redirect

titles =  dict()
titles["about"]= "Let's vetify the time"
titles["index"]= "Find out when your final exam is"


@app.route("/", methods=["GET","POST"])
def index():
    df, info = scrape("fall")
    if request.method == "POST":
        req = request.form

        # Since the AM PM thing is a slider- a checkbox really - if ampm is a key with the value 'on' then it is pm
        # if ampm is not a key, then the user has chosen AM
        if "ampm" in request.form.keys():
            print ("PM")
        print(request.form.get("time"))
        print(request.form.get("day"))

        return redirect(request.url)
    info = hi()
    return render_template("index.html", index = titles["index"], info = info)

@app.route("/about")
def about():
    return render_template("about.html", about = titles["about"])
