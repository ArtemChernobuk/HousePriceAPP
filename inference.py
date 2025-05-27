import re
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import sqlite3
import datetime

import optuna
import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
import time
import json

loaded_model = xgb.Booster()
loaded_model.load_model("models/model.json")

with open("models/best_features.json", "r") as fp:
    best_features = json.load(fp)

with open("models/target_mean.json", "r") as fp:
    target_mean = json.load(fp)

print(target_mean)

def inference_model(data):
    # Make a copy of the input data to avoid modifying the original
    inference = data.copy()


    for i in target_mean.keys():
        print(i)
        print(target_mean[i])
        print(list(inference[i.replace("_target_mean", "")])[0])
        print(target_mean[i][list(inference[i.replace("_target_mean", "")])[0]])
        inference[i] = [target_mean[i][list(inference[i.replace("_target_mean", "")])[0]]]

    print(inference)
    result = float(loaded_model.predict(xgb.DMatrix(inference[best_features]))[0])

    db = sqlite3.connect("base.db")
    c = db.cursor()

    db_submit = list(data.iloc[0])
    db_submit.append(result)


    placeholders = ", ".join("?" * len(db_submit))
    c.execute(f"INSERT INTO requests VALUES ({placeholders})", db_submit)


    print(inference.T)
    print(list(inference.iloc[0]))
    print(len(list(inference.iloc[0])))

    db.commit()
    db.close()
    return result