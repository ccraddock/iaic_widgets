import numpy as np
import pydicom as dicom
import os
import datetime
#import matplotlib.pyplot as plt
import glob
from collections import defaultdict
import pathlib
import time


def mask(image):
  pixels = image.pixel_array
  
  rows = pixels.shape[0]
  cols = pixels.shape[1]
  masked = np.zeros((rows, cols))
  mean = np.mean(pixels)
  for i in range((rows)):
    for j in range((cols)):
      if (not(mean * 1.2 >= pixels[i][j] >= mean * .6)):
        image.pixel_array[i][j]=0
  
  image.PixelData=image.pixel_array.tostring()
 
  
  return image


# store dictionary of images into new folder
def store(imagedict):
  pathlib.Path("../Dell/maskedimages").mkdir(exist_ok=True)
  
  for key in imagedict:
    imagelist = imagedict[key]
    pathlib.Path("../Dell/maskedimages/" + key).mkdir(exist_ok=True)
    for i in range(len(imagelist)):
      image = dicom.dcmread(imagelist[i])
      masked=mask(image)
      masked.save_as("../Dell/maskedimages/" + key + "/" + str(i) + "masked.dcm", write_like_original=True)


# scan and save according to patient name (returns dictionary of lists)
def scanPatientName():
  images = []
  images = glob.glob("**/*.dcm", recursive=True)
  
  print("scanning function, patient name")
  print()
  
  patient = defaultdict(list)
  
  for i in range(len(images)):
    read = dicom.read_file(images[i])
    if (str(read.PatientName) in patient):
      patient[str(read.PatientName)].append(images[i])
    else:
      newlist = []
      newlist.append(images[i])
      patient[str(read.PatientName)] = newlist
  return patient


# scan and save according to series description (returns dictionary of lists)
def scanSeriesDescription():
  print("scanning function, series description")
  images = []
  images = glob.glob("**/*.dcm", recursive=True)
  sequencename = defaultdict(list)
  
  for i in range(len(images)):
    read = dicom.read_file(images[i])
    
    if (str(read.SeriesDescription) in sequencename):
      sequencename[str(read.SeriesDescription)].append(images[i])
    else:
      newlist = []
      newlist.append(images[i])
      sequencename[str(read.SeriesDescription)] = newlist    
    
    # if ("misc" in sequencename):
    #   sequencename["misc"].append(images[i])
    # else:
    #   newl=[]
    #   newl.append(images[i])
    #   sequencename["misc"]=newl
  # store(sequencename)
  
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
    #os.system(command)


def rem():

  images=[]
  images=glob.glob("**/*.dcm", recursive=True)
  for image in images:
    print (image)
    os.remove(image)


def main():
  startTime = time.time()
  
  print("scanning function")
  print()
 
  seq = scanSeriesDescription()
  
  store(seq)

  sendback()

  rem()
  
  
  print('The script took {0} second !'.format(time.time() - startTime))


main()