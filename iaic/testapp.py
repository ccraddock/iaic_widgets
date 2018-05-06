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


studyID=""
def createLog():
  
  images = []
  images = glob.glob("./maskedimages/**/*.dcm", recursive=True)
  # studynamefile=open("studyname.txt", "w")
  
  studyimage=images[0]
  siread=pydicom.dcmread(studyimage)
  global studyID
  studyID=siread.StudyID
  
  ipfile = open("ip.txt", 'r')
  ip = ipfile.readline().strip()
  
  try:
    logs = pickle.load(open("logs.p", "rb"))
    for i in range(len(images)):
      now = datetime.datetime.now()
      date = now.strftime("%Y-%m-%d")
      
      if (ip in logs):
        
        if (date in logs[ip]):
          logs[ip][date].append(images[i])
        else:
          logs[ip][date] = []
          logs[ip][date].append(images[i])
      
      
      else:
        
        print("else")
        logs[ip] = {}
        logs[ip][date] = []
        logs[ip][date].append(images[i])
    
    pickle.dump(logs, open("logs.p", "wb"))
  
  except:
    logs = {}
    logs[ip] = {}
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    
    logs[ip][date] = []
    
    for i in range(len(images)):
      logs[ip][date].append(images[i])
    
    pickle.dump(logs, open("logs.p", "wb"))


def makecsv():
  arrdata = transform()
  
  ips = []
  dates = []
  imagelists = []
  studyNames=[]
  for i in range(len(arrdata)):
    ips.append(arrdata[i][0])
    dates.append(arrdata[i][1])
    imagelists.append(len(arrdata[i][2]))
    studyNames.append(studyID)
  # print(studyNames)
  myitems = [("IP", ips), ("Dates", dates), ("Images", imagelists), ("Study ID", studyNames)]
  
  df = pd.DataFrame.from_items(myitems)
  df.to_csv("logs.csv", index=False)


def transform():
  logs = pickle.load(open("logs.p", "rb"))
  arrdata = []
  for ip in logs:
    for date in logs[ip]:
      arr = []
      arr.append(ip)
      arr.append(date)
      arr.append(logs[ip][date])
      arrdata.append(arr)
  
  return arrdata


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
  createLog()
  makecsv()
  app.run_server(debug=True, host="0.0.0.0")
