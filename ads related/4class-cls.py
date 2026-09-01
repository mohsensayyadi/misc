#from google.cloud.bigtable.client import Client
from google.cloud.happybase import Connection
#from targeting.demographics_profile_pb2 import AgeInferenceProfile
#from protobuf_to_dict import protobuf_to_dict
import pandas as pd
from google.cloud import bigquery
#import seaborn as sns
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
#import shutil
#from IPython.core.display import display, HTML
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
#from snapml.dao import gdao
from sklearn.model_selection import train_test_split, KFold
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer, LabelEncoder
import sklearn
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import plot_confusion_matrix
from sklearn import tree
from sklearn.utils import resample
#from imxgboost.imbalance_xgb import imbalance_xgboost as imb_xgb
import datetime
import time


def defineTargetVar(row):
    if row['EXP_HHI'] == 'Household Income ($1,000-$24,999)':
        val = 0
    elif row['EXP_HHI'] == 'Household Income ($25,000-$49,999)':
        val = 0
    elif row['EXP_HHI'] == 'Household Income ($50,000-$74,999)':
        val = 1
    elif row['EXP_HHI'] =='Household Income ($75,000-$99,999)':
        val = 1
    elif row['EXP_HHI'] == 'Household Income ($100,000-$124,999)':
        val = 2
    elif row['EXP_HHI'] == 'Household Income ( $125,000-$149,999)':
        val = 2
    elif row['EXP_HHI'] == 'Household Income ($150,000-$174,999)':
        val = 3
    elif row['EXP_HHI'] == 'Household Income ($175,000-$199,999)':
        val = 3
    elif row['EXP_HHI'] == 'Household Income ($200,000-$249,999)':
        val = 3
    elif row['EXP_HHI'] == 'Household Income ($250,000+)':
        val = 3
    else:
        val = 3
    return val


def makeBalancedDF(dfObj):
    if 'label' not in list(dfObj.columns):
        dfObj['label'] = dfObj.apply(defineTargetVar, axis=1)
    df_majority = dfObj[dfObj.label == 0]
    df_minority = dfObj[dfObj.label == 4]

    print('minortiy size ', df_minority.shape)
    dfs = [df_minority]
    for i in [0, 1, 2, 3]:
        df_larger = dfObj[dfObj.label == i]
        # Downsample larger class
        df_larger_downsampled = resample(df_larger,
                                         replace=False, n_samples=df_minority.shape[0], random_state=123)
        dfs.append(df_larger_downsampled)

        print('new majority class size', df_larger_downsampled.shape)
    df_downsampled = pd.concat(dfs)
    print('size of balanced data set', df_downsampled.shape)

    return df_downsampled.sample(frac=1)


def scoreDecTree(dfObj, TopKFeatures, treeDepth):
    featuresList = list(dfObj.columns)
    featuresList.remove('EXP_HHI')
    featuresList.remove('user_id')
    featuresList.remove('zipcode')
    #featuresList.remove('postal_code')
    if 'label' in featuresList:
        featuresList.remove('label')
    else:
        # data = df.sample(n=50000, random_state=1)
        dfObj['label'] = dfObj.apply(defineTargetVar, axis=1)
    y = dfObj['label']
    one_hot_data = pd.get_dummies(dfObj[featuresList], drop_first=True)
    print('list of features', list(one_hot_data.columns))

    decTree = DecisionTreeClassifier(max_depth=treeDepth)
    decTree.fit(one_hot_data, dfObj['label'])
    if treeDepth < 4:
        tree_to_pseudo(decTree, list(one_hot_data.columns))

    clf = DecisionTreeClassifier(random_state=0)
    scores = cross_val_score(clf, one_hot_data, dfObj['label'], cv=5)
    print("cross validation scores", scores)
    colNames = list(one_hot_data.columns)
    imp = decTree.feature_importances_
    print(decTree.feature_importances_)

    ind = np.argsort(-decTree.feature_importances_)[:TopKFeatures]
    print('Top', TopKFeatures, 'important features')
    for i in range(TopKFeatures):
        print(colNames[ind[i]], ' ,  ', decTree.feature_importances_[ind[i]])

    print('Done')


def scoreRF(dfObj, TopKFeatures, treeDepth):
    featuresList = list(dfObj.columns)
    featuresList.remove('EXP_HHI')
    featuresList.remove('user_id')
    featuresList.remove('zipcode')
    #featuresList.remove('postal_code')
    if 'label' in featuresList:
        featuresList.remove('label')
    # data = df.sample(n=50000, random_state=1)
    dfObj['label'] = dfObj.apply(defineTargetVar, axis=1)
    y = dfObj['label']
    one_hot_data = pd.get_dummies(dfObj[featuresList], drop_first=True)
    print('list of features', list(one_hot_data.columns))

    decTree = RandomForestClassifier(max_depth=treeDepth)
    decTree.fit(one_hot_data, dfObj['label'])

    clf = RandomForestClassifier(random_state=0)
    scores = cross_val_score(clf, one_hot_data, dfObj['label'], cv=5)
    print("cross validation scores", scores)
    colNames = list(one_hot_data.columns)
    imp = decTree.feature_importances_
    print(decTree.feature_importances_)

    ind = np.argsort(-decTree.feature_importances_)[:TopKFeatures]
    print('Top', TopKFeatures, 'important features')
    for i in range(TopKFeatures):
        print(colNames[ind[i]], ' ,  ', decTree.feature_importances_[ind[i]])

    print('Done')


def scoreLGB(dfObj, TopKFeatures):
    featuresList = list(dfObj.columns)
    featuresList.remove('EXP_HHI')
    featuresList.remove('user_id')
    featuresList.remove('zipcode')
    # featuresList.remove('postal_code')
    if 'label' in featuresList:
        featuresList.remove('label')
    else:
        # data = df.sample(n=50000, random_state=1)
        dfObj['label'] = dfObj.apply(defineTargetVar, axis=1)
    y = dfObj['label']
    one_hot_data = pd.get_dummies(dfObj[featuresList], drop_first=True)
    print('list of features', list(one_hot_data.columns))

    kfold = KFold(n_splits=5)
    result = next(kfold.split(one_hot_data), None)

    train_x = one_hot_data.iloc[result[0]]
    train_y = dfObj['label'].iloc[result[0]]
    test_x = one_hot_data.iloc[result[1]]
    test_y = dfObj['label'].iloc[result[1]]

    train_data = lightgbm.Dataset(train_x, label=train_y)
    test_data = lightgbm.Dataset(test_x, label=test_y)

    parameters = {
        'application': 'binary',
        'objective': 'multiclass',
        'num_class': 4,
        'metric': 'multi_logloss',
        'is_unbalance': 'true',
        'boosting': 'gbdt',
        'num_leaves': 31,
        'feature_fraction': 0.5,
        'bagging_fraction': 0.5,
        'bagging_freq': 20,
        'learning_rate': 0.05,
        'verbose': 0
    }

    model = lightgbm.train(parameters,
                           train_data,
                           valid_sets=test_data,
                           num_boost_round=5000,
                           early_stopping_rounds=100)

    preds = model.predict(test_x)
    print("accuracy", accuracy_score(test_y, np.argmax(preds, axis=1)))
    print("macro F1", f1_score(test_y, np.argmax(preds, axis=1), average='macro'))
    print("F1 on each class", f1_score(test_y, np.argmax(preds, axis=1), average=None))

    return (train_x, train_y, test_x, test_y, model)

def scoreXGB(dfObj, TopKFeatures):
    featuresList = list(dfObj.columns)
    featuresList.remove('EXP_HHI')
    featuresList.remove('user_id')
    featuresList.remove('zipcode')
    #featuresList.remove('postal_code')
    if 'label' in featuresList:
        featuresList.remove('label')
    else:
        # data = df.sample(n=50000, random_state=1)
        dfObj['label'] = dfObj.apply(defineTargetVar, axis=1)
    y = dfObj['label']
    one_hot_data = pd.get_dummies(dfObj[featuresList], drop_first=True)
    print('list of features', list(one_hot_data.columns))

    kfold = KFold(n_splits=5)
    result = next(kfold.split(one_hot_data), None)

    train_x = one_hot_data.iloc[result[0]]
    train_y = dfObj['label'].iloc[result[0]]
    test_x = one_hot_data.iloc[result[1]]
    test_y = dfObj['label'].iloc[result[1]]
    unique, counts = np.unique(train_y, return_counts=True)
    print("labels in the training", dict(zip(unique,counts)))
    unique, counts = np.unique(test_y, return_counts=True)
    print("labels in the test", dict(zip(unique,counts)))
    #OLD [2,5,7,3] NEW:[2,2,6,9] for plain query for balanced query [2,1,2,3]
    weights = np.where(train_y == 0, 2, train_y)
    weights = np.where(weights == 1, 2, weights)
    weights = np.where(weights == 2, 6, weights)
    weights = np.where(weights == 3, 9, weights)
    #weights = np.where(weights == 4, 27, weights)
    print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)

    model = XGBClassifier(verbosity=1, colsample_bytree=0.8, subsample=0.8, max_depth=5, learning_rate=0.5,
                          objective='multi:softprob', n_jobs= 16)
    model.fit(train_x, train_y, weights)

    pred = model.predict(test_x)
    print("accuracy", accuracy_score(test_y, pred))
    print("macro F1", f1_score(test_y, pred, average='macro'))
    print("F1 on each class", f1_score(test_y, pred, average=None))
    modelCP = model
    scores = cross_val_score(model, one_hot_data, dfObj['label'], cv=5)
    print("cross validation scores", scores)
    colNames = list(one_hot_data.columns)
    imp = model.feature_importances_
    print("\n feature importance ")
    print(model.feature_importances_)

    ind = np.argsort(-model.feature_importances_)[:TopKFeatures]
    print('\nTop', TopKFeatures, ' important features')
    for i in range(TopKFeatures):
        print(colNames[ind[i]], ' ,  ', model.feature_importances_[ind[i]])

    print('Done')
    return (train_x, train_y, test_x, test_y, modelCP)


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
            print(indent, "if ( " + features[node] + " <= " + str(threshold[node]) + " ) {")
            if left[node] != -1:
                recurse(left, right, threshold, features, left[node], depth + 1)
                print(indent, "} else {")
                if right[node] != -1:
                    recurse(left, right, threshold, features, right[node], depth + 1)
                print(indent, "}")
        else:
            print(indent, "return " + str(value[node]))

    recurse(left, right, threshold, features, 0)

project = 'sc-targeting-measurement'
client = bigquery.Client()
def run_query(query):
    return client.query(query).result().to_dataframe()



SEED = 100
random.seed(SEED)
seed(SEED)
print('Started')

query = """
SELECT * except(app_profile, demographics, Conversion, attribution, app_ids, clusters, makes, report_date, latest_date, latest_ts, latest_days_ago)
FROM `sc-targeting-measurement.mosen_dev.HHI_features_raw_sparse`
where rand()<0.05
"""

t1 = time.time()

df = run_query(query)
print(df.shape)

df1 = df.fillna(0)

print(df1.shape)

train_x, train_y, test_x, test_y, model = scoreXGB(df1, 5)

d = time.time() - t1
print("--- %s seconds ---" % (d))
print("--- %s minutes ---" % (d/60))
print("--- %s hours ---" % (d/3600))
#scoreRF(df, 5, 20)

#df1 = makeBalancedDF(df1)

print('Done')

plot_confusion_matrix(model, test_x, test_y, normalize='true')
plt.show()