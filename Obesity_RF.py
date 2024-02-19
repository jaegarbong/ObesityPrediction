import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler,OneHotEncoder
from sklearn.metrics import classification_report

from warnings import filterwarnings
filterwarnings('ignore')
seed = 42

data = pd.read_csv("./data/train.csv")
df = data.copy()
df = df.drop(['id'],axis=1)

X = df.drop(["NObeyesdad"],axis=1)
y = df["NObeyesdad"]

unique_classes = ["Insufficient_Weight","Normal_Weight", "Overweight_Level_I","Overweight_Level_II","Overweight_Level_III","Obesity_Type_I","Obesity_Type_II","Obesity_Type_III"]  #Set the order here.
labels = {c: i for i, c in enumerate(unique_classes)}
y_encoded = y.apply(lambda x: labels[x])

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=seed)
ytrain_enc = y_train.apply(lambda x: labels[x])
ytest_enc = y_test.apply(lambda x: labels[x])


## preprocessing steps:
cat_features = X_train.select_dtypes(include=['object'])
num_features = X_train.select_dtypes(include=['int64','float64'])

# Round the numerical values upto two decimal numbers

num_features = num_features.astype('float16')  # Convert to float8
num_features = num_features.apply(lambda x:round(x,2))

# Get the names of the columns
cat_cols = cat_features.columns.to_list()
num_cols = num_features.columns.to_list()


## Create Pipelines
preprocessor = ColumnTransformer([
    ('categorical_encoder', OneHotEncoder(drop='first'),cat_cols),
    ('scaler', RobustScaler(with_centering=False),num_cols)
    ]   
)

rf_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier()),
])

param_grid = {
    "classifier__n_estimators": [100, 200, 300],
    "classifier__max_depth": [10, 15, 20, 25],
}

# KFold cross-validation with 5 folds
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(estimator=rf_pipeline, param_grid=param_grid, cv=kfold, scoring="accuracy")

# Fit the GridSearchCV
grid_search.fit(X_train, ytrain_enc)

# Print best parameters and score
print("Best parameters:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)

# Get the best model
best_model = grid_search.best_estimator_

## Make predictions on the test set
y_pred = best_model.predict(X_test)
y_pred_decoded = [unique_classes[i] for i in y_pred]

## Evaluate the model

report = classification_report(y_test, y_pred_decoded)
print(report)

from pickle import dump

with open("rf_classifier.pkl","wb") as f:
    dump(best_model,f)