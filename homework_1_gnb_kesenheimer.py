# -*- coding: utf-8 -*-
"""Homework_1_GNB_Kesenheimer

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oL36Co1B1dkq1cLgor-eN8WAA39jEpRD

#Prerequisites

## Import Libraries
Import required libraries for prerequisites.
"""

from google.colab import files
import pandas as pd
import io

"""##Import Data
Upload file, read data from csv file into dataset variable.
"""

uploaded = files.upload()

data_set = pd.read_csv(io.BytesIO(uploaded['SAKI Exercise 1 - Transaction Classification - Data Set.csv']), sep=';')

"""## Raw data evaluation

Data set, shape and recognized datatypes are displayed. 

"""

print(data_set)
print(data_set.shape)
print(data_set.dtypes)

"""#Manual data preprocessing

##Data manipulation
Column "Betrag" is recognized as data type Object. For later classification this column should be processed as a numeric feature, therefor a data type conversion is conducted. 

Data is printed out for verification of the applied functions.
"""

data_set["Betrag"] = data_set["Betrag"].str.replace(",", ".").astype(float)

print(data_set)
print(data_set.shape)
print(data_set.dtypes)

"""## Identify missing values
Values in column “Betrag” have different decimal separators. As only decimal separators are present in this column all comma separator are replaced by point separators. 
The function isna() returns, if a value is not or NaN and can be summed up to get the number of missing values per column. 
Data is printed out for verification of the applied functions.
"""

data_set.isna().sum()

data_set['Auftragskonto'] = data_set['Auftragskonto'].fillna(89990210.0)
data_set['Kontonummer'] = data_set['Kontonummer'].fillna('Unknown')
data_set['BLZ'] = data_set['BLZ'].fillna('Unknown')
data_set.isna().sum()

"""##Reshaping
Reshaping data set to X and Y sets. 
Shapes of newly created data set is printed, to verify successful slicing.Unique Classes are printed. 
"""

X = data_set.iloc[:,:11]
Y = data_set.iloc[:,11]


print('Data_Set Shape: ', data_set.shape)
print('X Shape: ', X.shape)
print('Y Shape: ', Y.shape)
print('Y_Classes', Y.unique())

"""#Gaussian Naive Bayes

Import required libraries for Gaussian Naive Bayes.
"""

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import GaussianNB
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
from collections import Counter

gnb = GaussianNB()

"""##Comparing OrdinalEncoder() to OneHotEncoder()
Both functions are implemented and validated against accuracy and weighted F1-Score to compare which encoder algorithm supports better classification of the data. For simplification reasons all features are handled at this stage as categorical features.

### Calculating results for OrdinalEncoder()
"""

enc = OrdinalEncoder()
ord_enc = enc.fit_transform(X)

#Split into Test and Training data set
#Fit the classifier
# Predict y_pred based on X_test
X_train, X_test, y_train, y_test = train_test_split(ord_enc, Y, test_size=0.2, random_state=42)
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)

#Result evaluation
print("Model Score: %.3f" % gnb.score(X_test, y_test))
print('Accuracy Score: %.3f' % metrics.balanced_accuracy_score(y_test, y_pred))
print('F1 Score weighted: %.3f' % metrics.f1_score(y_test, y_pred, average = 'weighted'))

"""### Calculating results for OneHotEncoder()

"""

#capture categorical features in list and name transformer
categorical_features = ['Auftragskonto','Buchungstag','Valutadatum','Buchungstext','Verwendungszweck','Beguenstigter/Zahlungspflichtiger', 'Kontonummer', 'BLZ', 'Betrag', 'Waehrung']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

#built preprocessor 
preprocessor = ColumnTransformer(transformers=[('cat', categorical_transformer, categorical_features)],sparse_threshold=0)

#Append classifier to preprocessing pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', GaussianNB())])

#Split into Test and Training data set
#Fit the classifier
# Predict y_pred based on X_test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

#Result evaluation
print("Model Score: %.3f" % clf.score(X_test, y_test))
print('Accuracy Score: %.3f' % metrics.balanced_accuracy_score(y_test, y_pred))
print('F1 Score weighted: %.3f' % metrics.f1_score(y_test, y_pred, average = 'weighted'))

"""##OneHotEncoder()

##Categorical and Numeric Features

Transforming column "Betrag" as a numeric feature instead of a categorical feature.
"""

#capture numeric features in list and name transformer
numeric_features = ['Betrag']
numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),('scaler', StandardScaler())])

#capture categorical features in list and name transformer
categorical_features = ['Auftragskonto','Buchungstag','Valutadatum','Buchungstext','Verwendungszweck','Beguenstigter/Zahlungspflichtiger', 'Kontonummer', 'BLZ', 'Waehrung']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

#built preprocessor 
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features),('cat', categorical_transformer, categorical_features)],sparse_threshold=0)

# Append classifier to preprocessing pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', GaussianNB())])

#Split into Test and Training data set
#Fit the classifier
# Predict y_pred based on X_test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

#Result evaluation
print("model score: %.3f" % clf.score(X_test, y_test))
print('Accuracy Score: %.3f' % metrics.balanced_accuracy_score(y_test, y_pred))
print('F1 Score weighted: %.3f' % metrics.f1_score(y_test, y_pred, average = 'weighted'))
metrics.plot_confusion_matrix(clf,X_test,y_test)
plt.show
print('_______')
print(metrics.classification_report(y_test,y_pred))

"""##Drop Date Columns"""

#capture numeric features in list and name transformer
numeric_features = ['Betrag']
numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),('scaler', StandardScaler())])

#capture categorical features in list and name transformer
categorical_features = ['Auftragskonto','Buchungstext','Verwendungszweck','Beguenstigter/Zahlungspflichtiger', 'Kontonummer', 'BLZ', 'Waehrung']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

#built preprocessor 
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features),('cat', categorical_transformer, categorical_features)],sparse_threshold=0)

# Append classifier to preprocessing pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', GaussianNB())])

#Split into Test and Training data set
#Fit the classifier
# Predict y_pred based on X_test
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

#Result evaluation
print("model score: %.3f" % clf.score(X_test, y_test))
print('Accuracy Score: %.3f' % metrics.balanced_accuracy_score(y_test, y_pred))
print('F1 Score weighted: %.3f' % metrics.f1_score(y_test, y_pred, average = 'weighted'))
metrics.plot_confusion_matrix(clf,X_test,y_test)
plt.show
print('_______')
print(metrics.classification_report(y_test,y_pred))

"""## Distribution of data across labels """

print(Counter(Y))