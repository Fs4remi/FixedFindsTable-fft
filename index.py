from flask import (Flask, render_template, request, flash)
import os
import pandas as pd
import re


CSV_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(CSV_FOLDER, 'reconstructedTable.csv')
df = pd.read_csv(file_path)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=('POST','GET'))
def index():
	if request.method == 'POST':
		ampm = request.form['ampm']
		days = request.form['days']
		start_time = request.form['start_time']
		time = int(re.findall("^[0-9]+",start_time)[0])
		if (time < 12) and (ampm[0] == 'p'):
			time += 12
		elif (time == 12) and (ampm[0] == 'a'):
			time = 0
		time -= 6 #'cause the CSV table got messed up indices
		reply = df.loc[time,days]
		if type(reply) == float:
			flash('Invalid class start time!')
		else:
			return render_template('response.html', reply=reply)
	return render_template('index.html')


if __name__ == "__main__":
	app.run()
