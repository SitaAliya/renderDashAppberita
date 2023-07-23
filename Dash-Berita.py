#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dash_table
from dash import Dash, dcc, html, Input, Output
#from jupyter_dash import JupyterDash # pip install dash (version 2.0.0 or higher)

#external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

app = Dash(__name__)
server=app.server

df=pd.read_json('all-berita-bp-short.json')
cleanup_nums = {"pariwisata_na":{3: 'None', 2:'Positif',0:'Negatif'},
                'ekspor_na':{1:'Netral',3:'None',2:'Positif',0:'Negatif'},
                'meeting_na':{3:'None',2:'Positif',0:'Negatif'},
                'kebijakan_na':{3:'None',2:'Positif',0:'Negatif'},
                'masyarakat_na':{1:'Netral',3:'None',0:'Negatif', 2:'Positif'}}
df = df.replace(cleanup_nums)
df=df[df['isi_x'].notna()]
def first_line(text):
    if len(text) > 100:
        text = text.partition('.')[0] + '.'
    return text
df['a'] = df['isi_x'].apply(lambda x: first_line(x))

#CHART PER ASPECT
##data dulu
value1 = pd.DataFrame(df['pariwisata_na'].value_counts())
value1 = value1.reset_index()  
value1.columns = ['Sentimen', 'Total']
value1 = value1[value1['Sentimen']!='None']

value2 = pd.DataFrame(df['ekspor_na'].value_counts())
value2 = value2.reset_index()  
value2.columns = ['Sentimen', 'Total']
value2 = value2[value2['Sentimen']!='None']

value3 = pd.DataFrame(df['meeting_na'].value_counts())
value3 = value3.reset_index()  
value3.columns = ['Sentimen', 'Total']
value3 = value3[value3['Sentimen']!='None']

value4 = pd.DataFrame(df['kebijakan_na'].value_counts())
value4 = value4.reset_index()  
value4.columns = ['Sentimen', 'Total']
value4 = value4[value4['Sentimen']!='None']

value5 = pd.DataFrame(df['masyarakat_na'].value_counts())
value5 = value5.reset_index()  
value5.columns = ['Sentimen', 'Total']
value5 = value5[value5['Sentimen']!='None']
colors = {'Positif':'green', 'Negatif':'red', 'Netral':'blue'}


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Analisis Sentimen Berbasis Aspek", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_news",
                 options=[
                     {"label": "Dailymail", "value": 'dailymail'},
                     {"label": "Reuters", "value": 'reuters'},
                     {"label": "CNN", "value": 'cnn'},
                     {"label": "CNBC", "value": 'cnbc'}],
                 multi=False,
                 value='cnn',
                 style={'width': "40%"}
                 ),

    html.Div(id='countainer', children=[]),
    html.Br(),
    
    #TABLE
    dash_table.DataTable(id='datable', data=df.to_dict('records'), style_data={'whiteSpace': 'normal','height': 'auto'},
                        style_cell={'textAlign': 'left'}, page_size=20),
    
    #CHART PER ASPEK
    html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.Div(children='''Pariwisata'''),
            dcc.Graph(id='graph1',figure=
                     px.bar(value1, x='Sentimen', y='Total', color='Sentimen')
    )], 
        className="two columns",style={"width":'20%', "margin": 0, 'display': 'inline-block'}),
        
        html.Div([
            html.Div(children='''Ekspor'''),
            dcc.Graph(id='graph2',figure=
                     px.bar(value2, x='Sentimen', y='Total', color='Sentimen')
    )],
        className="two columns",style={"width":'20%', "margin": 0, 'display': 'inline-block'}),
        
        html.Div([
            html.Div(children='''Diplomasi'''),
            dcc.Graph(id='graph3',figure=
                     px.bar(value3, x='Sentimen', y='Total', color='Sentimen')
   )],
        className="two columns", style={"width":'20%', "margin": 0, 'display': 'inline-block'}),
        
        html.Div([
            html.Div(children='''Kebijakan'''),
            dcc.Graph(id='graph4',figure=
                      px.bar(value4, x='Sentimen', y='Total', color='Sentimen')
   )],
        className="two columns",style={"width":'20%', "margin": 0, 'display': 'inline-block'}),
        
        html.Div([
            html.Div(children='''Masyarakat'''),
            dcc.Graph(id='graph5',figure=
                      px.bar(value5, x='Sentimen', y='Total', color='Sentimen')
                     )],
        className="two columns",style={"width":'20%', "margin": 0, 'display': 'inline-block'}),
    ], className='row')

    ])
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='countainer', component_property='children'),
     Output(component_id='datable', component_property='data')],
    [Input(component_id='slct_news', component_property='value')])
    
def update_graph(option_slctd):

    container = "Analisis Sentimen Berbasis Aspek pada Berita: {}".format(option_slctd)
    
    #TABEL
    dff = df.copy()
    dff = dff[dff["sumber"] == option_slctd]
    dff=dff[['Tahun','url','a','pariwisata_na', 'ekspor_na','meeting_na','kebijakan_na','masyarakat_na']]
    dff.rename(columns={'a':'Isi','pariwisata_na':'Pariwisata', 'ekspor_na': 'Ekspor','meeting_na':'Diplomasi',
                       'kebijakan_na':'Kebijakan','masyarakat_na':'Masyarakat'}, inplace=True)
    
    ##baru chart
    return container, dff.to_dict("records")

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)

