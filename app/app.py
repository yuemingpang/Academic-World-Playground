from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

import connectSQL as cs
import connectMongo as cm
import connectNeo4j as cn


app = Dash(__name__)

mySQL = cs.connectSQL()
MongoDB = cm.connectMongo()
Neo4j = cn.connectNeo4j()

app.layout = html.Div([

  html.Div([
    html.H1(
        children='Academic World Playground',
        style={'textAlign': 'center'}
    )
  ]),
  
  # Database Techniques: indexing, view, and trigger (implemented in SQL)
  html.Div([
    html.Br(),
    html.Button(id='indexing', children='Create Index', n_clicks=0),
    html.Button(id='view', children='Create View', n_clicks=0),
    html.Button(id='trigger', children='Create Trigger', n_clicks=0),
    html.Br(),
  ]),
  
  #1 SQL top 5 universities by its # of faculty associated (contain not exact mactch) with input keywords
  html.Div([
    html.H3(
        children='Top 5 universities of faculty associated with input keyword',
        style={'textAlign': 'center'}
    ),
    html.Label('Please enter the keyword:'),
    dcc.Input(id='input-1', value='data mining', type='text'),
    html.Button(id='button-1', children='Search', n_clicks=0),
    html.Br(),
    dcc.Graph(id='graph-1') #bar chart
  ]),
  
  #2 SQL top 5 popular faculty keywords in a University
  html.Div([
    html.H3(
        children='Top 5 keywords in the university',
        style={'textAlign': 'center'}
    ),
    html.Label('Please enter the university name:'),
    dcc.Input(id='input-2', value='University of illinois at Urbana Champaign', type='text'),
    html.Button(id='button-2', children='Search', n_clicks=0),
    html.Br(),
    dcc.Graph(id='graph-2') #pie chart
  ]),
  
  #3 MongoDB top 5 publications keywords by relevance (citation*score)
  html.Div([
    html.H3(
        children='Top 5 Publications of Input Keyword',
        style={'textAlign': 'center'}
    ),
    html.Label('Please enter the keyword:'),
    dcc.Input(id='input-3', value='database system', type='text'),
    html.Button(id='button-3', children='Search', n_clicks=0),
    html.Br(),
    dcc.Graph(id='graph-3') #bar chart
  ]),
  
  #4 Neo4j top 5 publication by citation#
  html.Div([
    html.H3(
        children='Top 5 most cited publications published in a specific year',
        style={'textAlign': 'center'}
    ),
    html.Label('Please select the year:'),
    dcc.Slider(
            min=1990,
            max=2022,
            step=1,
            marks={i: str(i) for i in range(1990, 2023)},
            value=2000,
            id='slider-4'
        ),
    html.Br(),
    dcc.Graph(id='graph-4') #scatter plot
  ]),
  
  #5 SQL update university photo URL
  html.Div([
    html.H3(
        children='Update the university photo',
        style={'textAlign': 'center'}
    ),
    html.Label('Please enter the university name:'),
    dcc.Input(id='input-5a', value='University of illinois at Urbana Champaign', type='text'),
    html.Button(id='button-5a', children='Display', n_clicks=0),
    html.Img(id='image-5'),
    html.Br(),
    html.Label('Please enter the new URL:'),
    dcc.Input(id='input-5b', value='None', type='text'),
    html.Button(id='button-5b', children='Replace', n_clicks=0)
  ]),
  
  #6 SQL update faculty photo URL
  html.Div([
    html.H3(
        children='Update the faculty photo',
        style={'textAlign': 'center'}
    ),
    html.Label('Please enter the faculty name:'),
    dcc.Input(id='input-6a', value='Kevin Chenchuan Chang', type='text'),
    html.Button(id='button-6a', children='Display', n_clicks=0),
    html.Img(id='image-6'),
    html.Br(),
    html.Label('Please enter the new URL:'),
    dcc.Input(id='input-6b', value='None', type='text'),
    html.Button(id='button-6b', children='Replace', n_clicks=0)
  ]),

  #7 close the database
  html.Div([
    html.P(id='placeholder1'),
    html.P(id='placeholder2'),
    html.P(id='placeholder3'),
    html.P(id='placeholder4'),
    html.P(id='placeholder5')
  ])
])

#callbacks:

# 3 Database Techniques:
@app.callback(Output('placeholder1', 'n_clicks'), Input('indexing', 'n_clicks'))
def create_index(n):
  mySQL.index()
  return n
  
@app.callback(Output('placeholder2', 'n_clicks'), Input('view', 'n_clicks'))
def create_view(n):
  mySQL.view()
  return n
  
@app.callback(Output('placeholder3', 'n_clicks'), Input('trigger', 'n_clicks'))
def create_trigger(n):
  mySQL.trigger()
  return n

#1
@app.callback(Output('graph-1', 'figure'),
              Input('button-1', 'n_clicks'),
              State('input-1', 'value'))
def update_widget_1(n, input):
  df = mySQL.widgetOne(input)
  fig = px.bar(df, x=df.columns.values[0], y=df.columns.values[1])
  return fig

#2
@app.callback(Output('graph-2', 'figure'),
              Input('button-2', 'n_clicks'),
              State('input-2', 'value'))
def update_widget_2(n, input):
  df = mySQL.widgetTwo(input)
  fig = px.pie(df, values='count', names='keyword', title='Top 5 keywords')
  return fig
  
#3  
@app.callback(Output('graph-3', 'figure'),
              Input('button-3', 'n_clicks'),
              State('input-3', 'value'))
def update_widget_3(n, input):
  df = MongoDB.widgetThree(input)
  fig = px.bar(df, x=df.columns.values[0], y=df.columns.values[1])
  return fig
  
#4  
@app.callback(Output('graph-4', 'figure'),
              Input('slider-4', 'value'))
def update_widget_4(input):
  df = Neo4j.widgetFour(input)
  fig = px.scatter(df, x=df.columns.values[0], y=df.columns.values[1])
  return fig
  
#5
@app.callback(Output('image-5', 'src'),
              Input('button-5a', 'n_clicks'),
              State('input-5a', 'value'))
def update_widget_5(n, input):
  path=mySQL.widgetFive(input)
  return path
@app.callback(Output('placeholder4', 'n_clicks'),
              Input('button-5b', 'n_clicks'),
              State('input-5a', 'value'),
              State('input-5b', 'value'))
def update_URL_5(n, name, url):
  mySQL.widgetUpdateFive(name, url)
  return n
  
#6
@app.callback(Output('image-6', 'src'),
              Input('button-6a', 'n_clicks'),
              State('input-6a', 'value'))
def update_widget_6(n, input):
  path=mySQL.widgetSix(input)
  return path
@app.callback(Output('placeholder5', 'n_clicks'),
              Input('button-6b', 'n_clicks'),
              State('input-6a', 'value'),
              State('input-6b', 'value'))
def update_URL_6(n, name, url):
  mySQL.widgetUpdateSix(name, url)
  return n


if __name__ == '__main__':
    app.run_server(debug=True)