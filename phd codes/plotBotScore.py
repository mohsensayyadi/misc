'''
Created on Mar 1, 2018

@author: msayyadi
'''


import numpy as np
import  matplotlib.pyplot as plt
import csv
import pandas as pd
from scipy import stats




botscores = []
humanscores = []
input = pd.read_csv("RFpredictions-caverlee-annotation.csv")

for i in range(1,len(input)):
    if int(input.iloc[i]["label"])==0:
        humanscores.append(input.iloc[i]["prob_1"])
    else:
        botscores.append(input.iloc[i]["prob_1"])
    
        

#input.iloc[2]["d"] 

#plt.plot(botscores)
#pd.DataFrame(botscores).plot(kind='density')
#pd.DataFrame(humanscores).plot(kind='density')
#plt.hist(botscores, bins=25, label='hst',color = "red")
#plt.hist(humanscores, bins=25, label='hst',color = "skyblue")
#plt.show()
print("finished")



density = stats.kde.gaussian_kde(botscores)
x = np.arange(0., 1, .05)
plt.plot(x, density(x))

density = stats.kde.gaussian_kde(humanscores)
plt.plot(x, density(x))

plt.show()
