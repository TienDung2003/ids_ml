import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import logging
from dotenv import load_dotenv
import os


load_dotenv()   

DATASETS_DIR = os.getenv("DATASETS_PATH")
DATATRAIN_DIR = Path(DATASETS_DIR ) 

data_train = pd.read_csv(DATATRAIN_DIR/ 'train_kdd.csv')
data_test = pd.read_csv(DATATRAIN_DIR/ 'test_kdd.csv')

X_train = data_train.drop(columns=['label'])
y_train = data_train['label'].astype(int)
X_test = data_test.drop(columns=['label'])
y_test = data_test['label'].astype(int)

cat_cols = ['protocol_type','service','flag']
num_cols = [c for c in X_train.columns if c not in cat_cols]
scaler = StandardScaler()

X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols]  = scaler.transform(X_test[num_cols])
X_train = pd.get_dummies(X_train, columns=cat_cols)
X_test  = pd.get_dummies(X_test, columns=cat_cols)
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

select_feature1 = ['duration',
                  'src_bytes',
                  'dst_bytes',
                  'flag_SF',
                  'flag_S0',
                  'count',
                  'srv_count',
                  'same_srv_rate',
                  'diff_srv_rate',
                  'srv_serror_rate',
                  'dst_host_srv_count',
                  'dst_host_same_srv_rate',
                  'dst_host_count',
                  'dst_host_diff_srv_rate',
                  'protocol_type_icmp',
                  'service_http']
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder




rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


import matplotlib.pyplot as plt
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score








nb = GaussianNB()

svm = SVC(
    kernel='rbf',
    probability=True,
    random_state=42
)



models = {
    # "Naive Bayes": nb,
    # "SVM": svm,
    "Random Forest": rf,
    
}

# In classification report và confusion matrix
# print("===== MLP Binary Classification =====")
# print(classification_report(y_test, y_pred_mlp))
# print(confusion_matrix(y_test, y_pred_mlp))
# import joblib
def evaluate_model(name,model, X_train, y_train, X_test, y_test):
    
    start_train = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_train
    # joblib.dump(model, f"{name}_model.pkl")
    # print(f"Model {name} đã được lưu thành công!")
    # Prediction time
    start_test = time.time()
    y_pred = model.predict(X_test)
    test_time = time.time() - start_test
    # Metrics
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    return acc, prec, rec, f1, train_time, test_time, tp, fp, tn, fn

import matplotlib
matplotlib.use("TkAgg")
results = []

for name, model in models.items():
    acc, prec, rec, f1, train_t, test_t, tp, fp, tn, fn = evaluate_model(
        name,model, X_train, y_train, X_test, y_test
    )

    print(f"\n=== {name} ===")
    print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")


    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1": f1,
        "Train_time(s)": train_t,
        "Test_time(s)": test_t
    })




results_df = pd.DataFrame(results)
print(results_df)

