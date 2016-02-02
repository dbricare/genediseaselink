from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import operator, os, datetime
from bokeh.plotting import figure, output_file, save, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components, autoload_static


app = Flask(__name__)


catclr = {'Ear, nose, and throat': '#aec7e8', 'Endocrine system (hormones)': '#e377c2', 'Lungs and breathing': '#c49c94', 'Heart and circulation': '#17becf', 'Reproductive system': '#f7b6d2', 'Eyes and vision': '#9467bd', 'Digestive system': '#ff9896', 'Bones, muscles, and connective tissues': '#ff7f0e', 'Skin, hair, and nails': '#d62728', 'Immune system': '#ffbb78', 'Food, nutrition, and metabolism': '#2ca02c', 'Cancers': '#8c564b', 'Mouth and teeth': '#98df8a', 'Kidneys and urinary system': '#c5b0d5', 'Not Available': '#eeeeee', 'Blood/lymphatic system': '#bcbd22', 'Brain and nervous system': '#1f77b4'}

disease_dict = {'all': 'All', 'digest': 'Digestive system', 'cancer': 'Cancers', 'skin': 'Skin, hair, and nails', 'heart': 'Heart and circulation', 'bone': 'Bones, muscles, and connective tissues', 'lung': 'Lungs and breathing', 'endocrine': 'Endocrine system (hormones)', 'brain': 'Brain and nervous system', 'reproductive': 'Reproductive system', 'kidney': 'Kidneys and urinary system', 'immune': 'Immune system', 'mouth': 'Mouth and teeth', 'metabolism': 'Food, nutrition, and metabolism', 'ent': 'Ear, nose, and throat', 'blood': 'Blood/lymphatic system', 'eye': 'Eyes and vision'}

# disease_dict['mental'] = 'Mental health and behavior'

dislist = sorted(disease_dict.items(), key=operator.itemgetter(1))

@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():  #remember the function name does not need to match the URL

    # Load plot data
#     dfall = pd.read_csv('GeneDiseaseMoreCats.csv')
    dfall = pd.read_csv('ThreeGDA.tsv',sep='\t')
    dfall.fillna(value='Not Available', inplace=True)
    
    # return user-selected data
    jump = ''
    sel = ''
    if request.method=='POST':
        jump = '<script> window.location.hash="box"; </script>'
        sel = request.form['selection']
        if sel != 'all':
            dfall = dfall[dfall['category']==disease_dict[sel]]
    
    yy = dfall['Number of genes']
    xx = dfall['score_total']

    # Generate colors for graphs
#     colorseq = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
#                 '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
#                 '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
#                 '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
#     colordark = colorseq[0::2]
#     colorlight = colorseq[1::2]
#     clrdrklt = colordark.copy()
#     clrdrklt.extend(colorlight)
#     uniqcat = dfall['category'].unique()
#     catclr = dict(zip(uniqcat.tolist(),clrdrklt[:len(uniqcat)]))
#     catclr['Not Available'] = '#eeeeee'

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
    t = os.path.getmtime('../genediseaselink-web/app.py')
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

