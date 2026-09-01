'''
Created on April 15, 2018

@author: mohsen sayyadi
'''
from __future__ import division  # floating point division
from numpy import genfromtxt
import pandas as pd
import csv
import random
import math
import numpy as np
import scipy.stats
from sklearn import metrics
import numpy as np
from sklearn.metrics import recall_score
from sklearn import tree
from sklearn import preprocessing
from sklearn.decomposition import PCA
import operator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def readInputFeatures(filePath):
    features = []
    
    with open(filePath) as f:
        lines = f.readlines()
    
    startRow = 0
    for line in lines[startRow:len(lines)]:
        try:
            tokens = line.replace("\n","").split(",")
            for token in tokens:
                features.append(token)
        except:
            continue
    return features

'''
this code reads numpy array(flat data set) and tries to train a model using adaboost/random forest 
and report its performance both on training set and test set. Also we perform cross data set classification
'''


def tree_to_pseudo(tree, feature_names):

    '''
    Outputs a decision tree model as if/then pseudocode
    
    Parameters:
    -----------
    tree: decision tree model
        The decision tree to represent as pseudocode
    feature_names: list
        The feature names of the dataset used for building the decision tree
    '''

    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, depth=0):
        indent = "  " * depth
        if (threshold[node] != -2):
            print(indent,"if ( " + features[node] + " <= " + str(threshold[node]) + " ) {")
            if left[node] != -1:
                recurse (left, right, threshold, features, left[node], depth+1)
                print(indent,"} else {")
                if right[node] != -1:
                    recurse (left, right, threshold, features, right[node], depth+1)
                print(indent,"}")
        else:
            print(indent,"return " + str(value[node]))

    recurse(left, right, threshold, features, 0)



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



def read_data(filePath,trainsize, testsize, useNormalization, usePCA, dropClusterIDColumn, classLabel,
               useTopFeatures, fiterSomeFeaturesBasedOnClass, inputFeatures):
    # header of input file
    # userid, label, predictive features
    # note that input should be suitable for numpy array e.g. no string like title of source or target should be included

    df = pd.read_csv(filePath, delimiter=',')

    if dropClusterIDColumn:
        df = df.loc[df['clusterID'] != 5] 
        df = df.drop(["clusterID"] , 1)
    if classLabel != -1:
        df = df.loc[df['label'] == classLabel]
    df = df.fillna(0)
    dataset = df.as_matrix(columns=None)
    print("dataset.shape", dataset.shape)
    featureset = range(0,1209)
    #randindices = np.random.randint(0,dataset.shape[0],trainsize+testsize)
    np.random.seed(0)
    if dropClusterIDColumn or classLabel != -1:
        randindices = np.array(random.sample(range(dataset.shape[0]), dataset.shape[0]))
    else:
        #randindices = np.array(random.sample(range(dataset.shape[0]), trainsize+testsize))
        #print("hi")
        randindices = np.array(range(0, dataset.shape[0]))
    #for index in sorted(randindices):
    #    print(index)
    finalCols = ["userID", "label" ]    
    if useTopFeatures:
        topN = 2
        #top100Features = readFeatureImportance("1209/caverlee_dataset_1209-FeatureImportance_coef.csv",topN)
        featureNames = readFeatureImportance("1209/featureImp/caverlee_RF_featureImportance_corDropped.csv",topN)
        finalCols.extend(featureNames)
        df = df[finalCols]
    elif fiterSomeFeaturesBasedOnClass:
        features = readFeatures("1209/header_1209.csv", [featureClass])
        df = df[features]
    elif inputFeatures:
        featureNames = readInputFeatures("1209/inputFeatures.csv")        
        print(featureNames)
        finalCols.extend(featureNames)
        df = df[finalCols]

    dataset = df.as_matrix(columns=None)    
    featureSize = dataset.shape[1]-2
    featureset = range(0,featureSize)
    
    #featureSize = dataset.shape[1]-1
    
    Xtrain1 = dataset[randindices[0:trainsize],2:featureSize+2]
    Xtrain2 = dataset[randindices[0:trainsize],0:featureSize+2]
    Xtrain = Xtrain1[:, featureset]
    #Xtrain2 = dataset[randindices[0:trainsize],0:numinputs+1]
    ytrain = dataset[randindices[0:trainsize],1]
    
    Xtest1 = dataset[randindices[trainsize:trainsize+testsize],2:featureSize+2]
    Xtest = Xtest1[:,featureset]
    ytest = dataset[randindices[trainsize:trainsize+testsize],1]
    Xtest2 = dataset[randindices[trainsize:trainsize+testsize],0:featureSize+2]
    
    #Xtrain = np.hstack((Xtrain, np.ones((Xtrain.shape[0],1))))
    #Xtest = np.hstack((Xtest, np.ones((Xtest.shape[0],1))))
    
    if useNormalization:
        min_max_scaler = preprocessing.MinMaxScaler()
        if Xtrain.shape[0] !=0:
            #Xtrain = min_max_scaler.fit_transform(Xtrain)
            Xtrain = preprocessing.normalize(Xtrain, norm='l2')
        if Xtest.shape[0] !=0:
            #Xtest = min_max_scaler.fit_transform(Xtest)
            Xtest = preprocessing.normalize(Xtest, norm='l2')
    if usePCA:
        pca = PCA(n_components=50)
        if Xtrain.shape[0] !=0:
            Xtrain = pca.fit_transform(Xtrain)
        if Xtest.shape[0] !=0:
            Xtest = pca.fit_transform(Xtest)
    print("Xtrain.shape", Xtrain.shape)
    print("Xtest.shape", Xtest.shape)
    return Xtrain, ytrain, Xtest,ytest, Xtest2, list(featureNames)

np.random.seed(0)
normalizeData = False
usePrincipalComponents = False
topFeatures = False
dsName = 'annotation'
filterSomeClassesofFeatures = False
dsPath = '1209/'+dsName+'_dataset_1209.csv'
dsPath2 = '1209/cresci-noCore-4BotClasses.csv'
readFromInputFeatureList = True

humans,ytrain,Xtest,ytest, xtest2_temp , featureList = read_data(dsPath2, 100, 18, normalizeData, usePrincipalComponents, False, 1, 
                                      topFeatures, filterSomeClassesofFeatures, inputFeatures=readFromInputFeatureList)

bots,ytrain,Xtest,ytest, xtest2_temp , featureList = read_data(dsPath2, 100, 18, normalizeData, usePrincipalComponents, False, 2, 
                                      topFeatures, filterSomeClassesofFeatures, inputFeatures=readFromInputFeatureList)

ff,ytrain,Xtest,ytest, xtest2_temp , featureList = read_data(dsPath2, 100, 18, normalizeData, usePrincipalComponents, False, 3, 
                                      topFeatures, filterSomeClassesofFeatures, inputFeatures=readFromInputFeatureList)


print(featureList)

humans_x =  humans[:,0]#np.array([1,2,3])
humans_y = humans[:,1]#2 * np.array([1,2,3])
humans_z = humans[:,2]#2 * np.array([1,2,3])

bots_x =  bots[:,0]#np.array([1,2,3])
bots_y = bots[:,1]#2 * np.array([1,2,3])
bots_z = bots[:,2]#2 * np.array([1,2,3])

ff_x =  ff[:,0]#np.array([1,2,3])
ff_y = ff[:,1]#2 * np.array([1,2,3])
ff_z =  ff[:,2]#np.array([1,2,3])
#y2 = 3 * np.array([1,2,3])
#area2 = np.ma.masked_where(r >= r0, area)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(humans_x, humans_y, humans_z, '.', color='r')

ax.plot(bots_x, bots_y, bots_z, '.', color='b')

ax.plot(ff_x, ff_y, ff_z, '.', color='g')

plt.xlabel(featureList[0])
plt.ylabel(featureList[1])
#plt.zlabel(featureList[2])

ax.legend()
plt.show()