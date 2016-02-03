from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import operator, os, datetime
from bokeh.plotting import figure, output_file, save, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components, autoload_static


app = Flask(__name__)


catclr = {'Not Available': '#eeeeee', 'Ear, nose, and throat': '#1f77b4', 'Lungs and breathing': '#ff9896', 'Blood/lymphatic system': '#aec7e8', 'Brain and nervous system': '#ff7f0e', 'Immune system': '#17becf', 'Mental health and behavior': '#c49c94', 'Heart and circulation': '#bcbd22', 'Kidneys and urinary system': '#e377c2', 'Food, nutrition, and metabolism': '#9467bd', 'Cancers': '#d62728', 'Eyes and vision': '#7f7f7f', 'Bones, muscles, and connective tissues': '#2ca02c', 'Reproductive system': '#98df8a', 'Digestive system': '#c5b0d5', 'Skin, hair, and nails': '#8c564b'}

disease_dict = {'all': 'All', 'digest': 'Digestive system', 'cancer': 'Cancers', 'skin': 'Skin, hair, and nails', 'heart': 'Heart and circulation', 'bone': 'Bones, muscles, and connective tissues', 'lung': 'Lungs and breathing', 'endocrine': 'Endocrine system (hormones)', 'brain': 'Brain and nervous system', 'reproductive': 'Reproductive system', 'kidney': 'Kidneys and urinary system', 'immune': 'Immune system', 'mouth': 'Mouth and teeth', 'metabolism': 'Food, nutrition, and metabolism', 'ent': 'Ear, nose, and throat', 'blood': 'Blood/lymphatic system', 'eye': 'Eyes and vision'}

disease_dict['mental'] = 'Mental health and behavior'

dislist = sorted(disease_dict.items(), key=operator.itemgetter(1))

@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():  #remember the function name does not need to match the URL

    # Load plot data
#     dfall = pd.read_csv('GeneDiseaseMoreCats.csv')
#     dfall = pd.read_csv('ThreeGDA.tsv',sep='\t')
    dfall = pd.read_csv('GDAallthree.tsv',sep='\t')
    dfall.fillna(value='Not Available', inplace=True)
    
    # return user-selected data
    jump = ''
    sel = ''
    if request.method=='POST':
        jump = '<script> window.location.hash="gdaplot"; </script>'
        sel = request.form['selection']
        if sel != 'all':
            dfall = dfall[dfall['category']==disease_dict[sel]]
    
    yy = dfall['Number of genes']
    xx = dfall['score_total']

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


    p = figure(plot_width=900, plot_height=600, tools=['box_zoom','pan','reset', 'save',hover], title="")
#     p.title_text_font = 'helvetica neue'
    p.title_text_font = 'Source Sans Pro'
    p.xaxis.axis_label = 'Strength of Association  ( Higher is Better )'
    p.yaxis.axis_label = 'Gene Associations Per Disease  ( Lower is Better )'
    p.xaxis.axis_label_text_font = 'Source Sans Pro'
    p.yaxis.axis_label_text_font = 'Source Sans Pro'


    p.circle('x', 'y', size=20, fill_alpha=0.8, color=dfall['color'], source=source, line_width=1, line_color='#000000')
    p.responsive = True

#     script, div = autoload_static(p, CDN, "")
    script, div = components(p)

    t = os.path.getmtime('app.py')
    updated = '{modt:%B} {modt.day}, {modt:%Y}'.format( modt=datetime.date.fromtimestamp(t) )

#     updated = 'February 2, 2016'

#     if request.method=='POST':
#         return render_template(url_for('index',_anchor='box'), script=script, div=div, 
#         dislist = dislist, updated=updated)
#     else:


    return render_template('index.html', script=script, div=div, 
    dislist=dislist, updated=updated, jumpscript=jump, sel=sel)        


if __name__ == "__main__":
    app.run(port=33507)

