'''
Created on Aug 31, 2018

@author: msayyadi
'''

import pandas as pd
import csv
import random
import math
import numpy as np
from sklearn.metrics import  pairwise
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import preprocessing
import operator
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


def read_data(filePath, classLabel, useNormalization, usePCA, useTopFeatures, inputFeatures):
    # header of input file
    # userid, label, predictive features
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included
    
    df = pd.read_csv(filePath, delimiter=',')
    if classLabel != -1:
        df = df.loc[df['label'] == classLabel] 
    df = df.drop(["user_friendFollowerRatio_SNR"] , 1)
    df = df.fillna(0)
    finalCols = ["userID", "label" ]
    if useTopFeatures:
        topN = 100
        top100Features = readFeatureImportance("1209/featImp/annotation_RF_featureImportance_corDropped.csv",topN)
        print(top100Features)
        finalCols.extend(top100Features)
        df = df[finalCols]
    elif inputFeatures:
        featureNames = readInputFeatures("1209/caverlee_tree3_features.csv")
        print(featureNames)
        finalCols.extend(featureNames)
        df = df[finalCols]
    #df.to_csv("100features-caverlee10k", encoding='utf-8', index=False)
    #df = df.loc[df['label'] ==1]
    dataset = df.as_matrix(columns=None)
    featureSize = dataset.shape[1]-2
    featureset = range(0,featureSize)    

        
    #randindices =  np.array(random.sample(range(dataset.shape[0]), trainsize+testsize))

    Xtest = dataset[:,2:featureSize+2]
    ytest = dataset[:,1]
    Xtest2 = dataset[:,0:featureSize+2]    
    if useNormalization:
        #min_max_scaler = preprocessing.MinMaxScaler()
        if Xtest.shape[0] !=0:
            #Xtest = min_max_scaler.fit_transform(Xtest)
            Xtest = preprocessing.normalize(Xtest, norm='l2')
    
    if usePCA:
        pca = PCA(n_components=50)
        if Xtest.shape[0] !=0:
            Xtest = pca.fit_transform(Xtest)

    
    print("Final data set shape:", Xtest.shape)
    return df, Xtest,ytest,Xtest2


def readFeatureImportance(filepath, k):
    importanceDict = {}

    with open(filepath) as f:
        lines = f.readlines()
    
    startRow = 1
    for line in lines[startRow:len(lines)]:
        try:
            feature, coef = line.replace("\n","").split(",")
            if 'user_friendFollowerRatio_SNR' in feature:continue
            importanceDict[feature] = float(coef)

        except:
            continue
        
    sorted_dict = sorted(importanceDict.items(), key=operator.itemgetter(1),reverse=True)
    
    return dict(sorted_dict[0:k]).keys()


def readInputFeatures(filepath):
    names = []
    with open(filepath) as f:
        lines = f.readlines()
    
    startRow = 0
    for line in lines[startRow:len(lines)]:
        try:
            tokens = line.replace("\n","").split(",")
            for feature in tokens:
                names.append(feature)
        except:
            continue
    
    return names


def saveNewDatasetWithClusterID(oldDataFrame, clusterIDs):
    oldDataFrame['clusterID'] = clusterIDs
    oldDataFrame.to_csv("caverlee-dataset-1209-withClusterID2.csv", encoding='utf-8', index=False)

interestedClass = -1

#read_data(filePath, classLabel, useNormalization, usePCA, useTopFeatures):
normalization = True
oldDf, Xtest,ytest,Xtest2 = read_data('1209/annotation_dataset_1209.csv', interestedClass, normalization, False, True, False)

clustersNum = 10

kmeans = KMeans(n_clusters=clustersNum, random_state=0).fit(Xtest)
#kmeans = DBSCAN(eps=0., min_samples=2).fit(Xtest)

#saveNewDatasetWithClusterID(oldDf, kmeans.labels_)

sampleSize = Xtest.shape[0]

cluster0Humans = 0
cluster0Bots = 0
cluster1Humans = 0
cluster1Bots = 0

#np.savetxt("kmeans_centers.csv", kmeans.cluster_centers_, delimiter=",",fmt='%10.5f')

kmeansVotes = {}

predictedFile=open("kmeans-caverlee_humans.csv", "w")
predictedFile.write("userid,label,clusterNum\n")

for i in range(0,sampleSize):
    clusterLabel = int(kmeans.labels_[i])
    label = int(ytest[i])
    if clusterLabel not in kmeansVotes.keys():
        kmeansVotes[clusterLabel] = {}
    if label in kmeansVotes[clusterLabel]:
        kmeansVotes[clusterLabel][label] = kmeansVotes[clusterLabel][label] + 1
    else:
          kmeansVotes[clusterLabel][label] = 1
          
    if kmeans.labels_[i]==0 and ytest[i]==0:
        cluster0Humans = cluster0Humans + 1
    elif kmeans.labels_[i]==0 and ytest[i]==1:
        cluster0Bots = cluster0Bots + 1
    elif kmeans.labels_[i]==1 and ytest[i]==1:
        cluster1Bots = cluster1Bots + 1
    elif kmeans.labels_[i]==1 and ytest[i]==0:
        cluster1Humans = cluster1Humans + 1
    predictedFile.write(str(Xtest2[i][0])+","+str(ytest[i])+","+str(kmeans.labels_[i])+"\n")
#print(kmeans.labels_)

print("cluster 0 humans:", cluster0Humans, "cluster 0 bots:", cluster0Bots)

print("cluster 1 humans:", cluster1Humans, "cluster 1 bots:", cluster1Bots)

print(sorted(kmeansVotes.items()))

if interestedClass == -1:
    labels = 'Human', 'Bot'
elif interestedClass == 1:
    labels = ['Bot']
else:
    labels = ['Human']
fig, subplots = plt.subplots(int(math.ceil(clustersNum/2)), 2)
colors = [ 'yellowgreen', 'lightcoral']
explode = (0.1, 0)  # explode 1st slice
i = 0
for key, value in sorted(kmeansVotes.items()): #key in kmeansVotes.keys():
    if interestedClass != -1:
        sizes = [int(kmeansVotes[key][interestedClass])]
    elif 0 in kmeansVotes[key] and 1 in kmeansVotes[key]:
        sizes = [int(kmeansVotes[key][0]), int(kmeansVotes[key][1])]
    elif 0 in kmeansVotes[key] and 1 not in kmeansVotes[key]:
        sizes = [int(kmeansVotes[key][0]) , 0]
    elif 0 not in kmeansVotes[key] and 1 in kmeansVotes[key]:
        sizes = [0, int(kmeansVotes[key][1])]
        
    subplots[int(i/2),int(i%2)].pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140 )
    subplots[int(i/2),int(i%2)].text(-0.1, 1,'Cluster '+str(key) + ", Size: "+ str(sum(sizes)))#title = 'cluster'
    i = i + 1
    
plt.show()