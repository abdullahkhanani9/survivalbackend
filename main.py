import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Load the titanic dataset
titanic_data = sns.load_dataset('titanic')

# Preprocess the data
td = titanic_data.copy()
td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
td.dropna(inplace=True)
td['sex'] = td['sex'].apply(lambda x: 1 if x == 'male' else 0)
td['alone'] = td['alone'].apply(lambda x: 1 if x == True else 0)

# Encode categorical variables
enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(td[['embarked']])
onehot = enc.transform(td[['embarked']]).toarray()
cols = ['embarked_' + val for val in enc.categories_[0]]
td[cols] = pd.DataFrame(onehot)
td.drop(['embarked'], axis=1, inplace=True)
td.dropna(inplace=True)

# Split data into train and test sets
X = td.drop('survived', axis=1)
y = td['survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a decision tree classifier
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

# Test the decision tree model
y_pred_dt = dt.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)
print('DecisionTreeClassifier Accuracy: {:.2%}'.format(accuracy_dt))

# Train a logistic regression model
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# Test the logistic regression model
y_pred_lr = logreg.predict(X_test)
accuracy_lr = accuracy_score(y_test, y_pred_lr)
print('LogisticRegression Accuracy: {:.2%}'.format(accuracy_lr))

# Define a new passenger
passenger = pd.DataFrame({
    'name': ['Abdullah Khanani'],
    'pclass': [1],
    'sex': ['male'],
    'age': [15],
    'sibsp': [1],
    'parch': [2],
    'fare': [512],
    'embarked': ['Q'],
    'alone': [False]
})

# Preprocess the new passenger data
new_passenger = passenger.copy()
new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == True else 0)
onehot = enc.transform(new_passenger[['embarked']]).toarray()
cols = ['embarked_' + val for val in enc.categories_[0]]
new_passenger[cols] = pd.DataFrame(onehot, index=new_passenger.index)
new_passenger.drop(['name', 'embarked'], axis=1, inplace=True)

# Predict survival probability for the new passenger using logistic regression
dead_proba, alive_proba = np.squeeze(logreg.predict_proba(new_passenger))
print('Death probability: {:.2%}'.format(dead_proba))
print('Survival probability: {:.2%}'.format(alive_proba))
