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
from datetime import datetime, timedelta
import pytz


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


    #dff = pd.read_csv(timespan+'_output.csv')
    from_date, to_date = get_start_and_end()

    if timespan == 'today':
        query = {"timestamp": {"$gte": from_date, "$lt": to_date}}
    else:
        from_date -= timedelta(days=100)
        query = {"timestamp": {"$gte": from_date, "$lt": to_date}}

    dff = pd.DataFrame(list(collection.find(query)))
    
    dff = dff.sort_values(["timestamp"]).reset_index(drop=True)
    dff['timestamp'] = pd.to_datetime(dff['timestamp']).dt.tz_localize('UTC').dt.tz_convert('Europe/Helsinki')
    
   

    
    temp_fig = px.line(dff, x = 'timestamp', y = 'temperature', title='Temperature inside',
                       labels={
                           "timestamp":"Time",
                           "temperature":"Temperature (°C)"                           
                           })
    
    
    
    hum_fig = px.line(dff, x = 'timestamp', y = 'humidity', title='Humidity inside',
                      labels={
                          "timestamp":"Time",
                          "humidity":"Humidity (%)"
                          })

    tempnow = "{}°C".format(dff.tail(1).temperature.to_string(index=False))
    #hum_fig.update_traces(line_color='#0000FF', selector=dict(type='scatter'))
    #temp_fig.update_traces(line_color='#FF0000', selector=dict(type='scatter'))
    temp_fig['data'][0]['line']['color']='rgb(255, 0, 0)'
    hum_fig['data'][0]['line']['color']='rgb(3, 0, 125)'
    return temp_fig,hum_fig,tempnow

def get_start_and_end():
    tz = pytz.timezone('Europe/Helsinki')
    today = datetime.now(tz=tz)
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(1)

    return start, end


if __name__ == '__main__':
    #app.run_server(debug=True,host="192.168.1.31", port=8050)
    app.run_server(debug=True,host='0.0.0.0',port=8050)
