import os

# Clear the TensorBoardX log directory to avoid conflicts
os.environ["TENSORBOARDX_LOGDIR"] = ""  
os.environ["TUNE_DISABLE_STRICT_METRIC_CHECKING"] = "1"

import ray
from ray import tune, train
import numpy as np
import sklearn    
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from ray.tune.logger import UnifiedLogger

# Initialize Ray
ray.init()

# Define a function to load data
def load_data():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Define a function to train a model
def train_model(config):
    X_train, X_test, y_train, y_test = load_data()
    clf = RandomForestClassifier(**config)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    # Report the mean_accuracy metric
    train.report({"_metric" : accuracy})  
    return accuracy

# Define the hyperparameter search space
search_space = {
    "n_estimators": tune.randint(50, 200),
    "max_depth": tune.randint(2, 10),
}

# Configure Ray Tune with default loggers
analysis = tune.run(
    train_model,
    config=search_space,
    num_samples=10,
    metric="_metric",
    mode="max",
    resources_per_trial={"cpu": 1},
    verbose=1,
)

#Get the best hyperparameters and accuracy
best_trial = analysis.get_best_trial(metric="_metric", mode="max")

if best_trial is not None:
    best_params = best_trial.config
    best_accuracy = best_trial.last_result.get("_metric")

    if best_accuracy is not None:
        print("Best hyperparameters:", best_params)
        print("Best accuracy:", best_accuracy)
    else:
        print("Mean accuracy not found in best trial's last result.")
else:
    print("No best trial found.")

# Shut down Ray
ray.shutdown()