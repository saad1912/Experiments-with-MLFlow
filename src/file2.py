import mlflow
import mlflow.sklearn

from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

import dagshub
dagshub.init(repo_owner='saad1912', repo_name='Experiments-with-MLFlow', mlflow=True)


mlflow.set_tracking_uri("https://dagshub.com/saad1912/Experiments-with-MLFlow.mlflow")
wine = load_wine()
X = wine.data
y = wine.target

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

max_depth = 3
n_estimators = 19


mlflow.set_experiment('Experiment-1')
with mlflow.start_run():
    rf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, random_state=42)
    rf.fit(X_train,y_train)
    
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    
    
    mlflow.sklearn.log_model(rf,'Random Forest Model')
    mlflow.log_metric('accuracy',accuracy)
    mlflow.log_param('max_depth',max_depth)
    mlflow.log_param('n_estimators',n_estimators)
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt = 'd', xticklabels=wine.target_names, yticklabels=wine.target_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    
    plt.savefig('Confusion-matrix.png')
    
    mlflow.log_artifact('Confusion-matrix.png')
    mlflow.log_artifact(__file__)
    mlflow.set_tags({"Author" : "Saad", "Project" : "Wine Classification"})
    
    
    print(accuracy)