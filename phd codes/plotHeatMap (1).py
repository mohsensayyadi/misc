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



def read_data(filePath,trainsize, testsize, featureSize):
    # header of inputfile
    # userid, label, predictive features
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included
    
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included
    oracle = {}
     
    df = pd.read_csv(filePath, delimiter=',')

    df = df.fillna(0)
    dataset = df.as_matrix(columns=None)
    
    featureset = range(0,featureSize)
    randindices = np.random.randint(0,dataset.shape[0],trainsize+testsize)
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
    oracleArray = dataset[randindices[trainsize:trainsize+testsize],1]
    
    #Xtrain = np.hstack((Xtrain, np.ones((Xtrain.shape[0],1))))
    #Xtest = np.hstack((Xtest, np.ones((Xtest.shape[0],1))))
    
    for i in range(0,len(dataset)):
        oracle[dataset[i,0]] = dataset[i,1]
        
    return Xtrain,ytrain,Xtest,ytest,oracleArray



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

def giveTreeVotes(model, bots, size, data):
    heatMap = np.zeros([size,len(rf.estimators_)])
    botVotes = 0
    count = 0
    for i in range(0,len(data)):
        if ytest[i]== (1-bots):
                continue
        if count == len(heatMap):break
        j = 0
        RfVote = model.predict(data[i:i+1,:])[0]
        if RfVote == (1-bots):
            print(i)
        for tree in model.estimators_:
            vote = tree.predict(data[i:i+1,:])[0]
            heatMap[count,j] = vote
            if vote==1:
                botVotes = botVotes + 1
            j = j + 1
        count = count + 1
    
    return heatMap
        

def plotHeatMapForBoth(model, typeStr, heatMapSize, data):
    heatMap = np.zeros([heatMapSize,len(rf.estimators_)])
    heatMap_humans = giveTreeVotes(model, 0, heatMapSize/2, data)
    heatMap_bots = giveTreeVotes(model, 1, heatMapSize/2, data)
    
    mergedHeatMap = np.concatenate((heatMap_humans, heatMap_bots) , axis=0)
        
    ax = sns.heatmap(mergedHeatMap, linewidth=0.5)
    #plt.subplots(figsize=(20,15))
    plt.title(' Votes of Caverlee Trees on ' + typeStr)
    plt.ylabel('Samples')
    plt.xlabel('Trees')
    
    plt.show()


def plotHeatMap(model, Bots, typeStr, heatMapSize, data):
    heatMap = np.zeros([heatMapSize,len(rf.estimators_)])
    botVotes = 0
    count = 0
    
    for i in range(0,len(data)):
        if ytest[i]== (1-Bots):
                continue
        if count == len(heatMap):break
        j = 0
        RfVote = model.predict(data[i:i+1,:])[0]
        if RfVote == (1-Bots):
            print(i)
        for tree in model.estimators_:
            vote = tree.predict(data[i:i+1,:])[0]
            heatMap[count,j] = vote
            if vote==1:
                botVotes = botVotes + 1
            j = j + 1
        count = count + 1
    
    
    #print("bot votes " , botVotes )
    #tree = rf.estimators_[1]
    '''plt.imshow(heatMap, cmap='Blues' , interpolation='nearest')
    plt.title('Votes of Caverlee Trees  on Annotation Humans')
    plt.ylabel('Samples')
    plt.xlabel('Trees')
    plt.show()
    '''
        
    ax = sns.heatmap(heatMap, linewidth=0.5)
    #plt.subplots(figsize=(20,15))
    plt.title(' Votes of Caverlee Trees on ' + typeStr)
    plt.ylabel('Samples')
    plt.xlabel('Trees')
    
    plt.show()


'''
a = np.ones((100, 100))
a[0,0] = 1
a[0,1] = 0
a[1,0] = 1
a[1,1] = 0
a[3,3] = 0

#plt.imshow(a, cmap='hot', interpolation='nearest')
#plt.show()
'''

featureNames = [ ] 

with open('1150featureslist.csv') as f:
    lines = f.readlines()

startRow = 0
for line in lines[startRow:len(lines)]:
    try:
        tokens = line.replace("\n","").split(",")
        for token in tokens:
            featureNames.append(token)
    except:
        continue

#featureNames = ['a', 'a1', 'b', 'c']
Xtrain,ytrain,XtestCav,ytestCav, trainSetOracle = read_data('caverlee-dataset.csv', 20000, 5000 , len(featureNames))

Xtrain2,ytrain2,Xtest,ytest, trainSetOracle = read_data('annotation-dataset.csv', 1800, 420, len(featureNames))

#rf = pickle.load(open("Caverlee RF model.pkl", 'rb'))
rf = RandomForestClassifier(n_estimators=100, oob_score=True)
#decTree = tree.DecisionTreeClassifier()
rf.fit(Xtrain, ytrain)    # e.g. X.shape is (trainsize,featureNum)  and Y.shape is (trainsize,)

score(Xtest, ytest, rf, "annotation in domain")

#botScore = rf.predict_proba(Xtrain[51:52,:])[0][1]
#print("bot score ", botScore)

#plotHeatMap(rf, 0, "annotation Humans", 100,  Xtest)

#plotHeatMap(rf, 1, "annotation bots", 100)

plotHeatMapForBoth(rf, "annotation DS",100, Xtest)

#plotHeatMapForBoth(rf, "Caverlee DS",100, XtestCav)


