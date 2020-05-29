from app import app
from app.scraper import scrape
import datetime
import re
import pandas

from flask import render_template, request, redirect

titles =  dict()
titles["about"]= "About this website"
titles["index"]= "Find out when your final exam is"
titles["error"]= "Page Not Found"

FINALS_LOOKUP_TABLE = None

@app.route("/", methods=["GET","POST"])
def index():
	global FINALS_LOOKUP_TABLE

	if FINALS_LOOKUP_TABLE is None:
		FINALS_LOOKUP_TABLE = pandas.read_csv("./app/lookup_table.csv", index_col=0)

	if request.method == "GET":
		return render_template("index.html", index = titles["index"], info1 = "", info2 = "", info3 = "")
	elif request.method == "POST":
		time = request.form.get("time")
		days = request.form.get("day")
		response1 = "For classes that meet " 
		response1 += days
		response1 += " starting at "
		response1 += time
		#convert time to number...
		time_list = re.findall("\d+", time)
		half_hour =  int(time_list[0]) * 100
		if int(time_list[1]) > 30:
			half_hour += 30
		# Since the AM PM thing is a slider- a checkbox really - if ampm is a key with the value 'on' then it is pm
		# if ampm is not a key, then the user has chosen AM
		if "ampm" in request.form.keys():
			response1 += " pm"
			if half_hour < 1200:
				half_hour += 1200
		else:
			response1 += " am"
		response2 ="The final exam is:"
		try:
			response3 = FINALS_LOOKUP_TABLE.loc[half_hour, days]
			if type(response3) != type("string"):
				raise KeyError
		except (KeyError):
			response1 = "There are no classes that meet "
			response1 += days
			response1 += " starting at "
			response1 += time
			if half_hour >= 1200:
				response1 += " pm"
			else:
				response1 += " am"
			response2 = ""
			response3 = ""
		return render_template("index.html", index = titles["index"], info1 = response1, info2 = response2, info3 = response3)

@app.route("/about")
def about():
	return render_template("about.html", about = titles["about"])

@app.errorhandler(404)
def error(e):
	return render_template("anyError.html", error = titles["error"])
