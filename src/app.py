import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import flask
import os
import pymongo


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
username = os.environ['MONGO_INITDB_ROOT_USERNAME']
password = os.environ['MONGO_INITDB_ROOT_PASSWORD']

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)


#available_indicators = ['today','last_month']
app.title = "Temperature Plot"
app.layout = html.Div(children=[
        html.H1(id='tempnow',style={'textAlign':'center','color':'red','fontSize': '68px'}),
        html.Div("Select timespan:"),
        html.Div([
            dcc.Dropdown(
                id='timespan',
                options=[{'label': 'Today', 'value': 'today'},{'label': 'This week', 'value': 'this_week'},{'label': 'This month', 'value': 'this_month'}],
                value='today'
            ),            
        ],
        style={'width': '15%', 'display': 'inline-block'}),

        dcc.Graph(
            id='temperature-plot'
        ),
        
        dcc.Graph(
            id='humidity-plot'
        )
    ])



@app.callback(
    Output('temperature-plot', 'figure'),
    Output('humidity-plot', 'figure'),
    Output('tempnow','children'),
    Input('timespan', 'value'))
def update_graph(timespan):

    myclient = pymongo.MongoClient(f"mongodb://{username}:{password}@mongodb:27017/")
    db = myclient.database
    collection = db.tempcollection


    # dff = pd.read_csv(timespan+'_output.csv')
    dff = pd.DataFrame(list(collection.find()))
    
    temp_fig = px.line(dff, x = 'timestamp', y = 'temperature', title='Temperature inside',
                       labels={
                           "timestamp":"Time",
                           "temperature":"Temperature (°C)"                           
                           })
    
    temp_fig.update_traces(line_color='#FF0000', selector=dict(type='scatter'))
    
    hum_fig = px.line(dff, x = 'timestamp', y = 'humidity', title='Humidity inside',
                      labels={
                          "timestamp":"Time",
                          "humidity":"Humidity (%)"                          
                          })
    
    hum_fig.update_traces(line_color='#0000FF', selector=dict(type='scatter'))
    tempnow = "{}°C".format(dff.tail(1).temperature.to_string(index=False))

    return temp_fig,hum_fig,tempnow

if __name__ == '__main__':
    #app.run_server(debug=True,host="192.168.1.31", port=8050)
    app.run_server(debug=True,host='0.0.0.0',port=8050)