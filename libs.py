# =========================
# Core
# =========================
import numpy as np
import pandas as pd

# =========================
# Visualization
# =========================
import matplotlib.pyplot as plt
# import seaborn as sns

# =========================
# Train / Validation
# =========================
from sklearn.model_selection import (
    train_test_split,
    KFold,
    cross_val_score
)

# =========================
# Preprocessing
# =========================
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    LabelEncoder,
    LabelBinarizer
)

# =========================
# Models
# =========================
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# =========================
# Metrics
# =========================
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss,
    classification_report
)

# =========================
# Imbalanced Data
# =========================
from sklearn.utils import resample

# =========================
# Utilities
# =========================
import pickle
import datetime
import time
import random


import json

with open("data.json", "r") as f:
    data = json.load(f)
