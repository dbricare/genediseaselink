from flask import Flask, render_template, request, redirect, flash
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, save, show
from bokeh.resources import CDN
from bokeh.embed import components
import os, re


app = Flask(__name__)

# Format for JSON call:
# https://www.quandl.com/api/v3/datasets/CBOE/VIX.json?auth_token=M1JzmCxzCx-pQ5vUtUFL

authkey = 'M1JzmCxzCx-pQ5vUtUFL'
baseurl = 'https://www.quandl.com/api/v3/datasets/CBOE/'
suffixurl = '.json?auth_token='+authkey

codes = pd.read_csv('vix-codes.csv')

@app.route('/')
def main():
	return redirect('/index')


@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		idx = str.upper(request.form['inputticker'])
		p = re.compile('\W')
		idx = p.sub('',idx)
		if idx not in codes.Ticker.values:
			msg = "Ticker '{}' not found in 'Volatility Index and Ticker' table".format(idx)
			return render_template('index.html', errormsg=msg, codetable=codes.to_html(index=False, justify='left'))
		else:
			return redirect('/results', code=307)
	return render_template('index.html', codetable=codes.to_html(index=False, justify='left'))


@app.route('/results', methods=['GET','POST'])
def results():  #remember the function name does not need to match the URL
	idx = str.upper(request.form['inputticker'])
	p = re.compile('\W')
	idx = p.sub('',idx)
	
	call = baseurl+idx+suffixurl
	rj = requests.get(call).json()
	rj = rj['dataset']
	data = pd.DataFrame(rj['data'], columns=rj['column_names'])	

	x = pd.to_datetime(data.iloc[:,0])
	y = data.iloc[:,-1]

	toollist = "pan,box_zoom,reset,save,resize"

	output_file("templates/output.html", title='Volatility Index Graph')
	p = figure(x_axis_label=data.columns[0], y_axis_label=data.columns[-1], \
	x_axis_type="datetime", tools=toollist, plot_width=800, plot_height=500)
	p.line(x, y, line_width=1, line_color="CornflowerBlue")
	p.title = codes.Name.values[codes.Ticker.values==idx][0]
	p.responsive = True

	script, div = components(p)

	return render_template('output.html', script=script, div=div)


if __name__ == "__main__":
# 	port = int(os.environ.get("PORT", 5000))
# 	app.run(host='0.0.0.0', port=port, debug=True)
	app.run(port=33507)

