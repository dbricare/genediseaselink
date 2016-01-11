from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, save, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components
from datetime import date


app = Flask(__name__)


@app.route('/')
def main():
	return redirect('/index')


@app.route('/index', methods=['GET'])
def index():  #remember the function name does not need to match the URL

	# Load plot data
	dfall = pd.read_csv('GeneDiseaseMoreCats.csv')
	dfall.fillna(value='Not Available', inplace=True)
	yy = dfall['Number of genes']
	xx = dfall['score']

	# Generate colors for graphs
	colorseq = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
				'#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
				'#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
				'#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
	uniqcat = dfall['category'].unique()
	catclr = dict(zip(uniqcat.tolist(),colorseq[:len(uniqcat)]))
	catclr['Not Available'] = '#eeeeee'

	# Scatter points for better readability
	np.random.seed(1)
	rndm = (np.random.random(yy.shape) - 0.5) * 0.8


	# Generate plot
	output_file("templates/index.html")

	dfall['color'] = dfall['category'].map(lambda x: catclr[x])

	source = ColumnDataSource(
			data=dict(
				x=xx,
				y=yy+rndm,
				genes=yy,
				desc=dfall['diseaseName'],
				cat=dfall['category']
			)
		)

	hover = HoverTool(tooltips=[("Disease", "@desc"), ("Score", "$x"), ("Genes", "@genes"),("Category", "@cat")])


	p = figure(plot_width=900, plot_height=600, tools=['pan','box_zoom','reset', 'save','resize',hover], title="Strength of Gene-Disease Association")
	p.title_text_font = 'helvetica neue'
	p.xaxis.axis_label = 'Score'
	p.yaxis.axis_label = 'Number of Genes'
	p.xaxis.axis_label_text_font = 'helvetica neue'
	p.yaxis.axis_label_text_font = 'helvetica neue'


	p.circle('x', 'y', size=20, fill_alpha=0.8, color=dfall['color'], source=source, line_width=2)
	p.responsive = True

	script, div = components(p)
	updated=date.today().strftime('%Y-%b-%d')

	return render_template('index.html', script=script, div=div, updated=updated)


if __name__ == "__main__":
	app.run(port=33507)

