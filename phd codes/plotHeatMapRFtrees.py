'''
Created on May 15, 2018

@author: msayyadi
'''

from __future__ import division  # floating point division
from numpy import genfromtxt
import pandas as pd
import matplotlib.pyplot as plt
import csv
import random
import math
import numpy as np
import scipy.stats
from sklearn import linear_model, datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import numpy as np
from sklearn.metrics import recall_score
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score
from sklearn import tree
import operator
from operator import itemgetter
import seaborn as sns
import pickle
from bokeh.charts.builders.heatmap_builder import HeatMap
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster

def readFeatures(filepath, useAllFeatures):
    features = []
    excludeFeatures = []
    with open(filepath) as f:
        lines = f.readlines()
    
    startRow = 0
    for line in lines[startRow:len(lines)]:
        try:
            tokens = line.replace("\n","").split(",")
            for token in tokens:
                if not useAllFeatures:
                    if "network_" in token or "friend_" in token:#or 1==0:
                        excludeFeatures.append(token)
                    else:
                        features.append(token)
                else:
                    features.append(token)
        except:
            continue
    return features,excludeFeatures

def read_data(filePath,trainsize, testsize):
    # header of input file
    # userid, label, predictive features
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included
    
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included

    df = pd.read_csv(filePath, delimiter=',')

    fullFeatureList, excludeFeaturesList = readFeatures("header_1209.csv", True)

    df = df.fillna(0)
    print(df.shape)
    df = df.drop(excludeFeaturesList, 1)
    dataset = df.as_matrix(columns=None)
    
    featureset = range(0,len(fullFeatureList)-2)
    #randindices = np.random.randint(0,dataset.shape[0],trainsize+testsize)
    randindices = np.array(random.sample(range(dataset.shape[0]), trainsize+testsize))
    featureSize = dataset.shape[1]-1
    
    Xtrain1 = dataset[randindices[0:trainsize],2:featureSize+1]
    Xtrain2 = dataset[randindices[0:trainsize],0:featureSize+1]
    Xtrain = Xtrain1[:, featureset]
    #Xtrain2 = dataset[randindices[0:trainsize],0:numinputs+1]
    ytrain = dataset[randindices[0:trainsize],1]
    
    Xtest1 = dataset[randindices[trainsize:trainsize+testsize],2:featureSize+1]
    Xtest = Xtest1[:,featureset]
    ytest = dataset[randindices[trainsize:trainsize+testsize],1]
    Xtest2 = dataset[randindices[trainsize:trainsize+testsize],0:featureSize+1]
    
    #Xtrain = np.hstack((Xtrain, np.ones((Xtrain.shape[0],1))))
    #Xtest = np.hstack((Xtest, np.ones((Xtest.shape[0],1))))
    print(Xtrain.shape)
    print(Xtest.shape)
    
    return Xtrain,ytrain,Xtest,ytest,Xtest2




def score( trainset, trainsetY, model, typeString):
    if len(trainset) ==0:
        return
    pred = model.predict(trainset)
    scoreclf = model.score(trainset, trainsetY) # prints the accuracy in training set
    print("Accuracy " + typeString, scoreclf)
    evalMatrix = precision_recall_fscore_support(trainsetY, pred, average='macro')
    print(" prec, recall, f1score are ", evalMatrix)
    confidenceMatrix = model.predict_proba(trainset)
    fpr, tpr, thresholds = metrics.roc_curve(trainsetY, pred, pos_label=1)
    areaUnderROC = metrics.auc(fpr, tpr)
    print("area under ROC for "  + typeString +  " "+ str(areaUnderROC))

    pred_prob = confidenceMatrix[:,1]
    fpr, tpr, thresholds = metrics.roc_curve(trainsetY, pred_prob)
    areaUnderROC = metrics.auc(fpr, tpr)
    print("area under ROC  "+ typeString+" using probability is : " + str(areaUnderROC))
    
    predictionsConfidence = {} 
    for i in range(0,len(trainset)):
        conf = abs( confidenceMatrix[i][0]- confidenceMatrix[i][1])
        predictionsConfidence[i] = conf
    
    return predictionsConfidence,pred, areaUnderROC

def giveTreeVotes(model, data):
    heatMap = np.zeros([data.shape[0],len(rf.estimators_)])
    botVotes = 0
    for i in range(0,len(data)):
        j = 0
        for tree in model.estimators_:
            vote = tree.predict(data[i:i+1,:])[0]
            heatMap[i,j] = vote
            j = j + 1
    
    return heatMap
        

def saveVotesOfTrees( heatMapMatrix, dsStr):
    i = 0
    f = open('output/trees/'+dsStr+'_trees_TreeVotes.csv','w')
    line = "treeID"
    for i in range(0,heatMapMatrix.shape[0]):
        line = line +",sample"+str(i)
    f.write(line+"\n")
    for i in range(0,heatMapMatrix.shape[1]):
        #print("tree_"+str(i) , rf.feature_importances_)
        line = str(i)
        for j in range(0,heatMapMatrix.shape[0]):
            line = line + ","+ str( heatMapMatrix[j,i])
        f.write(line+"\n")
    f.close()

def plotHeatMap_new(model, typeStr, heatMapSize, data_x, data_y):
    #heatMap = np.zeros([heatMapSize,len(rf.estimators_)])
    Y = sch.linkage(data_x, method='complete')
    Z = sch.dendrogram(Y, orientation='top')
    index = Z['leaves']
    data_x = data_x[index,:]
    plt.cla()
    
    
    ticksLabels = []
    for i in range(0,heatMapSize):
        ticksLabels.append('*')

    
    heatMap = giveTreeVotes(model,  data_x)
    
    #mergedHeatMap = np.concatenate((heatMap_humans, heatMap_bots) , axis=0)
        
    ax = sns.heatmap(heatMap, linewidth=0.10, yticklabels=ticksLabels)
    
    for i in range(0, heatMapSize):
        if data_y[i] == 1:
            plt.gca().get_yticklabels()[i].set_color('red')
        else:
            plt.gca().get_yticklabels()[i].set_color('blue')

    #plt.subplots(figsize=(20,15))
    plt.title(' Votes of Trees on ' + typeStr)
    plt.ylabel('Samples')
    plt.xlabel('Trees')
    
    plt.show()
    
    return heatMap


dsName = 'kevin'
dsPath = '1209/'+dsName+'_dataset_1209.csv'

heatMapSize = 100
Xtrain,ytrain,XtestCav,ytestCav,Xtest2 = read_data(dsPath, 418, heatMapSize)

#rf = pickle.load(open("Caverlee RF model.pkl", 'rb'))
rf = RandomForestClassifier(n_estimators=100, oob_score=True)

rf.fit(Xtrain, ytrain)    # e.g. X.shape is (trainsize,featureNum)  and Y.shape is (trainsize,)

#score(Xtest, ytest, rf, "annotation in domain")

matrix = plotHeatMap_new(rf, "annotation DS",heatMapSize, XtestCav, ytestCav)

saveVotesOfTrees(matrix, dsName)
#plotHeatMapForBoth(rf, "Caverlee DS",100, XtestCav)
