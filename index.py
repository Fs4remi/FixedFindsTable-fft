from flask import (Flask, render_template, request)


app = Flask(__name__)

@app.route('/', methods=('POST','GET'))
def index():
	if request.method == 'POST':
		reply = "TEST test TEST"
		return render_template('response.html', reply=reply)
	else:
		return render_template('index.html')


if __name__ == "__main__":
	app.run()
