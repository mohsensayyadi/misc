from scipy import stats
import pandas as pd
import csv
import random
import math
import numpy as np
from sklearn.metrics import  pairwise
import pandas as pd
from scipy import stats
import  matplotlib.pyplot as plt
import random
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
from sklearn import preprocessing
from scipy.stats import gaussian_kde
import operator


def read_data(filePath, classLabel, size, randomSamples, useTopFeatures, dropClusterIDColumn, clusterNum):
    # header of input file
    # userid, label, predictive features
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included

    df = pd.read_csv(filePath, delimiter=',')

    if classLabel != -1:
        df = df.loc[df['label'] ==classLabel]
    if dropClusterIDColumn:
        df = df.loc[df['clusterID'] == clusterNum] 
        df = df.drop(["clusterID"] , 1)
    if useTopFeatures:
        topN = 100
        finalCols = ["userID", "label" ]
        top100Features = readFeatureImportance("1209/caverlee_dataset_1209-FeatureImportance_coef.csv",topN)
        print(top100Features)
        finalCols.extend(top100Features)
        df = df[finalCols]
    else:
        df = df.drop(["user_friendFollowerRatio_SNR"] , 1)
    df = df.fillna(0)
    #df = df.loc[df['label'] ==0]
    dataset = df.as_matrix(columns=None)
    
    if randomSamples:
        if size > dataset.shape[0]:
            randindices = np.array(random.sample(range(dataset.shape[0]), dataset.shape[0]))
        else:
            randindices = np.array(random.sample(range(dataset.shape[0]), size))
    else:
        randindices = range(0,dataset.shape[0])
    #featureset = range(0,1208)
    if useTopFeatures:
        featureset = range(0,topN)
        featureSize = 100
    else:
        featureSize = dataset.shape[1]-2
        featureset = range(0,featureSize)
    
    
    #randindices = np.random.randint(0,dataset.shape[0],trainsize+testsize)
    
    #featureSize = dataset.shape[1]-1
    
    Xtrain1 = dataset[randindices,2:featureSize+2]
    Xtrain2 = dataset[randindices,0:featureSize+2]
    Xtrain = Xtrain1[:, featureset]
    #Xtrain2 = dataset[randindices[0:trainsize],0:numinputs+1]
    ytrain = dataset[randindices,1]
    print("Final Xtrain shape", Xtrain.shape)    
    return Xtrain,ytrain


def readFeatureImportance(filepath, k):
    importanceDict = {}

    with open(filepath) as f:
        lines = f.readlines()
    
    startRow = 1
    for line in lines[startRow:len(lines)]:
        try:
            feature, coef = line.replace("\n","").split(",")
            importanceDict[feature] = float(coef)

        except:
            continue
        
    sorted_dict = sorted(importanceDict.items(), key=operator.itemgetter(1),reverse=True)
    
    return dict(sorted_dict[0:k]).keys()


def bhattacharyya_distance(V1, V2, eps = 1e-10):
    return math.sqrt(abs(1 - np.sum(np.sqrt(np.multiply(V1, V2))) / math.sqrt(V1.mean()*V2.mean()*V1.size*V2.size)))


def computePairWideHelinger(ar1, ar2):
    distArray = np.zeros([ar1.shape[0], ar2.shape[0]])
    for i in range(0, ar1.shape[0]):
        for j in range(0, ar2.shape[0]):
            distArray[i][j] = bhattacharyya_distance(ar1[i], ar2[j])
            
    
    
    return distArray
    
    
    


def selectRandomCells(npArray, useNormalization, twoDiffSets):
    if useNormalization:
        #min_max_scaler = preprocessing.MinMaxScaler()
        #npArray = min_max_scaler.fit_transform(npArray)
        npArray = preprocessing.normalize(npArray, norm='l2')
    samples = []
    for i in range(0,len(npArray)):
        if twoDiffSets:
            lowerBound = 0
        else:
            lowerBound = i
        for j in range(lowerBound,len(npArray)):
            if i ==j and not twoDiffSets:continue
            if random.randint(0,10) < 12:
                samples.append(npArray[i][j])
    
    return samples


def plotDensityChart(data, color, title):
    density = gaussian_kde(data)
    x_d = np.linspace(0, np.max(data), 50)
    #set the covariance_factor lower means more detail
    density.covariance_factor = lambda : .015
    density._compute_covariance()
    if title == "Bots":
        plt.plot(x_d,density(x_d), color,  label=title , linestyle='--', dashes=(5, 1))
    else:
        plt.plot(x_d,density(x_d), color,label=title)
    

def plotHist(data, titleStr):
    #n, bins, patches = plt.hist(x=b, bins='auto', color='#0504aa',                          alpha=0.7, rwidth=0.85)
    plt.hist(data, bins=200)
    #plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(titleStr)
    #plt.text(23, 45, r'$\mu=15, b=3$')
    #maxfreq = n.max()
    # Set a clean upper y-axis limit.
    #plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()


def printStatistics(data, str):
    print("statistics for " + str)
    print("length " , len(data))
    print("Mean" , np.mean(np.array(data)))
    print("standard deviation" , np.std(np.array(data)))

metricName = "euclidean"
normalization = True
#euclidean
useClusterNum = True
#Xtrain,ytrain,Xtest,ytest = read_data("1209/caverlee-dataset-1209.csv", 10000, 0)
dsName = '1209/caverlee-humans-dataset-1209-withClusterID.csv'
topFeaures = True
clsLabel = 0
clsName = 'Human'

bots_0,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 0)
botsSim0 = pairwise.pairwise_distances(bots_0, metric=metricName)
b0 = selectRandomCells(botsSim0, normalization, False)

bots_1,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 1)
botsSim1 = pairwise.pairwise_distances(bots_1, metric=metricName)
b1 = selectRandomCells(botsSim1, normalization, False)

bots_2,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 2)
botsSim2 = pairwise.pairwise_distances(bots_2, metric=metricName)
b2 = selectRandomCells(botsSim2, normalization, False)

bots_3,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 3)
botsSim3 = pairwise.pairwise_distances(bots_3, metric=metricName)
b3 = selectRandomCells(botsSim3, normalization, False)

bots_4,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 4)
botsSim4 = pairwise.pairwise_distances(bots_4, metric=metricName)
b4 = selectRandomCells(botsSim4, normalization, False)

bots_5,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 5)
botsSim5 = pairwise.pairwise_distances(bots_5, metric=metricName)
b5 = selectRandomCells(botsSim5, normalization, False)

bots_6,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 6)
botsSim6 = pairwise.pairwise_distances(bots_6, metric=metricName)
b6 = selectRandomCells(botsSim6, normalization, False)

bots_7,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 7)
botsSim7 = pairwise.pairwise_distances(bots_7, metric=metricName)
b7 = selectRandomCells(botsSim7, normalization, False)

bots_8,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 8)
botsSim8 = pairwise.pairwise_distances(bots_8, metric=metricName)
b8 = selectRandomCells(botsSim8, normalization, False)

bots_9,ytrain = read_data(dsName, clsLabel , 100, True, topFeaures, useClusterNum, 9)
botsSim9 = pairwise.pairwise_distances(bots_9, metric=metricName)
b9 = selectRandomCells(botsSim9, normalization, False)






#plotHist(hb, "human bots")
'''
plotDensityChart(b0, 'black', clsName+"_0")
plotDensityChart(b1 , 'r', clsName+"_1")
plotDensityChart(b2 , 'y', clsName+"_2")
plotDensityChart(b3 , 'orange', clsName+"_3")
plotDensityChart(b4 , 'pink', clsName+"_4")
'''
plotDensityChart(b5 , 'black', clsName+"_5")
plotDensityChart(b6 , 'r', clsName+"_6")
plotDensityChart(b7 , 'orange', clsName+"_7")
plotDensityChart(b8 , 'pink', clsName+"_8")
plotDensityChart(b9, 'yellow', clsName+"_9")

#plotDensityChart(hb)
#plotDensityChart(h2b2)
plt.legend(loc='upper right')
plt.title('Caverlee')
plt.show()

