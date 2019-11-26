from flask import Flask, render_template, request, flash
import os
import pandas as pd
import re

CSV_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(CSV_FOLDER, 'templates/reconstructedTable.csv').replace("\\","/")
df = pd.read_csv(file_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.debug = True

@app.route('/', methods =('POST','GET'))
def index():
	if request.method == 'POST':
		ampm = request.form['ampm']
		days = request.form['days']
		start_time = request.form['start_time']
		time = int(re.findall("^[0-9]+",start_time)[0])
		
		if(ampm[0] == 'p') and (time != 12):
			time += 12
		#cases before 6 am, or after 10 pm, or midnight
		if ((time < 6) or (time > 21)) or ((time == 12) and (ampm[0] =='a')):
			flash ('Invalid class start time')
		else:
			time -= 6
			reply = df.loc[time,days]
			if type(reply) == float:
				flash ('Invalid class start time')
			else:
				flash(reply)
	return render_template('home.html')

@app.route('/learn')
def learn_to_verify_time():
	return render_template('learn.html')

if __name__ == '__main__':
	app.run()
