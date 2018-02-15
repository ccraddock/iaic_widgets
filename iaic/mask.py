import numpy as np
import dicom
import os
import datetime
import matplotlib.pyplot as plt
# from glob import glob
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# import scipy.ndimage
# from skimage import morphology
# from skimage import measure
# from skimage.transform import resize
# from sklearn.cluster import KMeans
# from plotly import __version__
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# from plotly.tools import FigureFactory as FF
# from plotly.graph_objs import *
import pandas as pd

# data_dir="C:/Users/Swanand/Desktop/School/UT/Research/Dell/phantom/PHANNIE_PHANTOM_2015-11-24_173708/Despot_1_-SAG_002"
# slices=[]
# for s in os.listdir(data_dir):
#   completepath=os.path.join(data_dir, s)
#   # print(completepath)
#   slices.append(dicom.read_file(str(completepath), force=True))
#
# now=datetime.datetime.now()
# time=now.strftime("%Y-%m-%d %H:%M")
#
# name_of_file="log"
# completeName= os.path.join(data_dir,name_of_file+".txt")
# logFile= open("log.txt", "w")
# print(slices[0].PatientName)
# logFile.writelines("Patient Name : "+str(slices[0].PatientName))

image=dicom.read_file("image6.dcm")

pixels=image._get_pixel_array()

rows= pixels.shape[0]
cols=pixels.shape[0]
masked=np.zeros((rows,cols))
mean=np.mean(pixels)
for i in range((rows)):
  for j in range((cols)):
    if (mean*1.2>=pixels[i][j]>=mean*.6):
      masked[i][j]=pixels[i][j]

image.save_as("image6masked.dcm", write_like_original=True)

imageMasked=dicom.read_file("image6masked.dcm")
imageMasked.PatientName=str(imageMasked.PatientName)+"Masked"
print(imageMasked.PatientName)

# print(pixels[100])



fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax1.imshow(pixels)
ax2 = fig.add_subplot(1,2,2)
ax2.imshow(masked)
plt.show()

# logFile.close()
# print(slices)