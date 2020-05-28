from app import app
from app.scraper import scrape
import datetime

from flask import render_template, request, redirect

titles =  dict()
titles["about"]= "Let's vetify the time"
titles["index"]= "Find out when your final exam is"


EXPIRY_DATE = None
LOOKUP_TABLE = None

@app.route("/", methods=["GET","POST"])
def index():
	global EXPIRY_DATE
	global LOOKUP_TABLE

	#choose the correct finals table! yay!
	today = datetime.date.today()
	if EXPIRY_DATE is None or today > EXPIRY_DATE:
		season = "fall"
		if today.month <= 6:
			season = "spring"
		elif today.month <= 9:
			season = "summer"
		LOOKUP_TABLE, EXPIRY_DATE = scrape(season)

	if request.method == "POST":
		print("such a post!")
		req = request.form
		response = "For classes that meet " 
		response += req.get("day")
		response += " starting at "
		response += req.get("time") + " "
		# Since the AM PM thing is a slider- a checkbox really - if ampm is a key with the value 'on' then it is pm
		# if ampm is not a key, then the user has chosen AM
		if "ampm" in request.form.keys():
			response += "p"
		else:
			response += "a"
		response += "m"
		response2 ="The final exam is normally on "
		#input lookup stuff here!
		response2 += "Monday, May 13 at 2:45 pm to 4:45 pm"

		return render_template("index.html", index = titles["index"], info1 = response, info2 = response2)
	else:
		return render_template("index.html", index = titles["index"], info1 = "", info2 = "")

@app.route("/about")
def about():
	return render_template("about.html", about = titles["about"])
