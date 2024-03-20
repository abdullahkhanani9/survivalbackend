from flask import Flask, request, jsonify
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)

# Load the logistic regression model
logreg = LogisticRegression()
# Load the one-hot encoder
enc = OneHotEncoder(handle_unknown='ignore')

# Load the Titanic dataset
import seaborn as sns
titanic_data = sns.load_dataset('titanic')

# Preprocess the Titanic dataset
def preprocess_data(data):
    data.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
    data.dropna(inplace=True)
    data['sex'] = data['sex'].apply(lambda x: 1 if x == 'male' else 0)
    data['alone'] = data['alone'].apply(lambda x: 1 if x == True else 0)
    enc.fit(data[['embarked']])
    onehot = enc.transform(data[['embarked']]).toarray()
    cols = ['embarked_' + val for val in enc.categories_[0]]
    data[cols] = pd.DataFrame(onehot)
    data.drop(['embarked'], axis=1, inplace=True)
    data.dropna(inplace=True)

preprocess_data(titanic_data)

# Train the logistic regression
