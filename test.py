import numpy as np
import os

os.chdir('D:/user/Desktop/Game_of_Life')
filename= "data.txt"
data= np.genfromtxt(filename,dtype=int)
data[2][3]=10
print(data)