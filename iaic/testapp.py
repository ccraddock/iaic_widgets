import dash

from dash.dependencies import Input, Output

import dash_core_components as dcc

import dash_html_components as html

import dash_table_experiments as dt

import pandas as pd
import glob
import pickle
import datetime
import plotly
import plotly.graph_objs as go

from plotly.tools import FigureFactory as ff
import plotly.figure_factory
import pydicom




app = dash.Dash()

Image_Logs = pd.read_csv('logs.csv')

dataframes = {
  
  'Image_Logs': Image_Logs}


def get_data_object(user_selection):
  """

  For user selections, return the relevant in-memory data frame.

  """
  
  return dataframes[user_selection]


status = open("status.txt", "r").readline()

app.layout = html.Div([
  
  html.H4('Image Analysis Logs'),
  html.Div(children='''
            check status of app
        ''' + status),
  
  html.Label('Report type:', style={'font-weight': 'bold'}),
  
  dcc.Dropdown(
    
    id='field-dropdown',
    
    options=[{'label': df, 'value': df} for df in dataframes],
    
    value='Image_Logs',
    
    clearable=False
  
  ),
  
  dt.DataTable(
    
    # Initialise the rows
    
    rows=[{}],
    
    row_selectable=False,
    
    filterable=True,
    
    sortable=True,
    
    id='table'
  
  )

], className='container')


@app.callback(Output('table', 'rows'), [Input('field-dropdown', 'value')])
def update_table(user_selection):
  """

  For user selections, return the relevant table

  """
  
  df = get_data_object(user_selection)
  
  return df.to_dict('records')


app.css.append_css({
  
  'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
  
})

if __name__ == '__main__':
  # createLog()
  # makecsv()
  app.run_server(debug=True, host="0.0.0.0")