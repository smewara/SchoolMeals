import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np

class LogisticRegressionClassifier:
    def __init__(self, data, categorical_features=[]):
        self.data = data
        self.categorical_features = categorical_features
        self.X_train, self.X_test, self.y_train, self.y_test = self._split_data()
        self.model = self._build_pipeline()

    def _split_data(self, test_size=0.2, random_state=42):
        data_no_missing = self.data.dropna()
        X = data_no_missing.drop('target', axis=1)
        y = data_no_missing['target']
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def _build_pipeline(self):
        # Create a preprocessor using ColumnTransformer and OneHotEncoder
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), self.categorical_features)
            ],
            remainder='passthrough'
        )

        # Create a pipeline with logistic regression
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression())
        ])

        return model

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        accuracy = metrics.accuracy_score(self.y_test, y_pred)
        precision = metrics.precision_score(self.y_test, y_pred, average='weighted')
        recall = metrics.recall_score(self.y_test, y_pred, average='weighted')
        print(f'Accuracy: {accuracy:.2f}')
        print(f'Precision: {precision:.2f}')
        print(f'Recall: {recall:.2f}')

    def predict(self, new_data):
        return self.model.predict(new_data)