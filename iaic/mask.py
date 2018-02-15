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
# import pandas as pd

#look for dicom images and scan them into a list of images 
def scan ():


	data_dir="insert data directory"
	slices=[]
	for s in os.listdir(data_dir):
	  completepath=os.path.join(data_dir, s)
	  # print(completepath)
	  slices.append(dicom.read_file(str(completepath), force=True))

	now=datetime.datetime.now()
	time=now.strftime("%Y-%m-%d %H:%M")

	name_of_file="log_"+time+".txt"
	completeName= os.path.join(data_dir,name_of_file+".txt")
	logFile= open(name_of_file, "w")
	print(slices[0].PatientName)
	logFile.writelines("Patient Name : "+str(slices[0].PatientName))

	return slices


#takes in image and applies a mask to it
def mask(image):
	pixels=image._get_pixel_array()

	rows= pixels.shape[0]
	cols=pixels.shape[1]
	masked=np.zeros((rows,cols))
	mean=np.mean(pixels)
	for i in range((rows)):
	  for j in range((cols)):
	    if (mean*1.2>=pixels[i][j]>=mean*.6):
	      masked[i][j]=pixels[i][j]

	image.save_as("imagemasked.dcm", write_like_original=True)

	imageMasked=dicom.read_file("imagemasked.dcm")
	imageMasked.PatientName=str(imageMasked.PatientName)+"Masked"
	print(imageMasked.PatientName)
	fig = plt.figure()
	ax1 = fig.add_subplot(1,2,1)
	ax1.imshow(pixels)
	ax2 = fig.add_subplot(1,2,2)
	ax2.imshow(masked)
	plt.show()

	return imageMasked

#plots the original image and the masked image side by side
# def show(image):

# 	masked=mask(image)
	


def main():

	imagename=input("Image name?")

	image=dicom.read_file(imagename)

	masked=mask(image)

	

main()

	

	# print(pixels[100])



	

# logFile.close()
# print(slices)