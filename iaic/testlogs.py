import glob
import datetime
import pickle
import plotly
import plotly.graph_objs as go
import pandas as pd
from plotly.tools import FigureFactory as ff
import plotly.figure_factory




def createLog():

  images=[]
  images=glob.glob("./maskedimages/**/*.dcm", recursive=True)
  ipfile=open("ip.txt", 'r')
  ip=ipfile.readline().strip()
  

  try:
    logs= pickle.load(open("logs.p", "rb"))
    for i in range (len(images)):
      now = datetime.datetime.now()
      date=now.strftime("%Y-%m-%d")

      if (ip in logs):

        

        if (date in logs[ip]):
          logs[ip][date].append(images[i])
        else:
          logs[ip][date]=[]
          logs[ip][date].append(images[i])


      else:
        
        print("else")
        logs[ip]={}
        logs[ip][date]=[]
        logs[ip][date].append(images[i])

    pickle.dump(logs, open("logs.p", "wb"))

  except:
    logs={}
    logs[ip]={}
    now = datetime.datetime.now()
    date=now.strftime("%Y-%m-%d")

    logs[ip][date]=[]


    for i in range (len(images)):

      logs[ip][date].append(images[i])

    pickle.dump(logs, open("logs.p", "wb"))
  
# def plot():
#
#   arrdata=transform()
#
#   ips=[]
#   dates=[]
#   imagelists=[]
#   for i in range (len(arrdata)):
#
#       ips.append(arrdata[i][0])
#       dates.append(arrdata[i][1])
#       imagelists.append(len(arrdata[i][2]))
#
#
#   myitems=[("IP", ips), ("Dates", dates), ("Images", imagelists)]
#
#
#   df= pd.DataFrame.from_items(myitems)
#   df.to_csv("logs.csv", index=False)
#   # table=plotly.figure_factory.create_table(df)
#   #
#   #
#   #
#   # plotly.offline.plot(table)
  
def plotwithpandas():
  arrdata = transform()
  
  ips = []
  dates = []
  imagelists = []
  for i in range(len(arrdata)):
    ips.append(arrdata[i][0])
    dates.append(arrdata[i][1])
    imagelists.append(len(arrdata[i][2]))
  
  myitems = [("IP", ips), ("Dates", dates), ("Images", imagelists)]
  
  df = pd.DataFrame.from_items(myitems)
  df.to_csv("logs.csv", index=False)
  
  trace= go.Table(
    header=dict(values=df.columns[1:],
                fill=dict(color="#ffb833 "),
                align=['left']*5),
    cells=dict(values=[df.IP, df.Dates, df.Images],
               fill=dict(color='#F5F8FF'),
               align = ['left'] * 5))
  data=[trace]
  return data
  # plotly.offline.plot(data)


def plotgraph():
  arrdata = transform()
  
  ips = []
  dates = []
  imagelists = []
  for i in range(len(arrdata)):
    ips.append(arrdata[i][0])
    dates.append(arrdata[i][1])
    imagelists.append(len(arrdata[i][2]))
  
  myitems = [("Dates", dates), ("Images", imagelists)]
  
  df = pd.DataFrame.from_items(myitems)
  
  trace1=go.Scatter(
    x=dates,
    y=imagelists,
    mode="lines+markers",
    name="Images"
  )
  data=[trace1]
  
  # plotly.offline.plot(data)
  return data

def transform():
  logs=pickle.load(open("logs.p", "rb"))
  arrdata=[]
  for ip in logs:
    for date in logs[ip]:
      arr=[]
      arr.append(ip)
      arr.append(date)
      arr.append(logs[ip][date])
      arrdata.append(arr)

  

  return arrdata



def main():
  #createLog()
  # plotwithpandas()
  # transform()
  plotgraph()

main()