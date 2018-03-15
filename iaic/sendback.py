import os
import glob

def main():
  
  images=[]
  images = glob.glob("./maskedimages/**/*.dcm", recursive=True)
  print (len(images))
  infile= open("ip.txt", "r")
  ip= infile.readline().strip()
  
  for i in range (len(images)):
  
    command="storescu "+ip+" 4443 "+"'"+images[i]+"'"
    #print (command)
    os.system(command)
 
main()

