import numpy as np
import pydicom as dicom
import os
import datetime
#import matplotlib.pyplot as plt
import glob
from collections import defaultdict
import pathlib
import time
import pandas as pd
import pickle


def mask(image):
  pixels = image.pixel_array
  
  rows = pixels.shape[0]
  cols = pixels.shape[1]
  masked = np.zeros((rows, cols))
  mean = np.mean(pixels)
  for i in range((rows)):
    for j in range((cols)):
      if (not(mean * .2 >= pixels[i][j] )):
        image.pixel_array[i][j]=0
  
  image.PixelData=image.pixel_array.tostring()
 
  
  return image


# store dictionary of images into new folder
def store(imagedict):
  pathlib.Path("./maskedimages").mkdir(exist_ok=True)
  # print(imagedict)
  for key in imagedict:
    imagelist = imagedict[key]
    # print(imagelist)
    pathlib.Path("./maskedimages/" + key).mkdir(exist_ok=True)
    for i in range(len(imagelist)):
      image = dicom.dcmread(imagelist[i])
      image.ImageComments = image.ImageComments+(" ,Processed")
      # print(image.ImageComments)
      
      masked=mask(image)
      masked.save_as("./maskedimages/" + key + "/" + str(i) + "masked.dcm", write_like_original=True)



# scan and save according to series description (returns dictionary of lists)
def scanSeriesDescription():
  print("scanning function, series description")
  images = []
  images = glob.glob("*.dcm", recursive=False)
  sequencename = defaultdict(list)
  
  for i in range(len(images)):
    read = dicom.read_file(images[i])
    
    if (str(read.SeriesDescription) in sequencename):
      sequencename[str(read.SeriesDescription)].append(images[i])
    else:
      newlist = []
      newlist.append(images[i])
      sequencename[str(read.SeriesDescription)] = newlist    
    
  return sequencename

def sendback():
  images=[]
  images = glob.glob("./maskedimages/**/*.dcm", recursive=True)
  print (len(images))
  infile= open("ip.txt", "r")
  ip= infile.readline().strip()
  
  for i in range (len(images)):
  
    command="storescu "+ip+" 4443 "+"'"+images[i]+"'"
    print (command)
    os.system(command)


def rem():

 
  images=[]
  images=glob.glob("*/*.dcm", recursive=False)
  for image in images:
    print (image)
    os.remove(image)
  images =glob.glob("*/*/*.dcm")
  for image in images:
    print(image)
    os.remove(image)
  images =glob.glob("*.dcm")
  for image in images:
    print(image)
    os.remove(image)


studyID = ""


def createLog():
  images = []
  images = glob.glob("./maskedimages/**/*.dcm", recursive=True)
  # studynamefile=open("studyname.txt", "w")
  
  studyimage = images[0]
  siread = dicom.dcmread(studyimage)
  global studyID
  studyID = siread.StudyID
  
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
  studyNames = []
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


def main():
  startTime = time.time()
  
  file=open("status.txt", "w")
  file.writelines("Busy")
  
  print("scanning function")
  print()
 
  seq = scanSeriesDescription()
  
  store(seq)
  createLog()
  makecsv()

  sendback()
  
  
  
  rem()

  file = open("status.txt", "w")
  file.writelines("Ready")
  print('The script took {0} second !'.format(time.time() - startTime))
  # os.system("python testapp.py")


main()