# Import necessary libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns

# Define the TitanicRegression class
class TitanicRegression:
    def __init__(self):
        self.dt = None
        self.logreg = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.encoder = None

    def initTitanic(self):
        titanic_data = sns.load_dataset('titanic')
        # Clean data
        self.clean_data(titanic_data)

    def clean_data(self, data):
        # Preprocess the data
        data.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        data.dropna(inplace=True) # Drop rows with at least one missing value, after dropping unuseful columns
        data['sex'] = data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        data['alone'] = data['alone'].apply(lambda x: 1 if x == True else 0)

        # Encode categorical variables
        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(data[['embarked']])
        onehot = enc.transform(data[['embarked']]).toarray()
        cols = ['embarked_' + val for val in enc.categories_[0]]
        data[cols] = pd.DataFrame(onehot)
        data.drop(['embarked'], axis=1, inplace=True)
        data.dropna(inplace=True) # Drop rows with at least one missing value, after preparing the data
    def predict_survival(self, data):
        try:
            passenger = pd.DataFrame([data]) 
            passenger['sex'] = passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
            passenger['alone'] = passenger['alone'].apply(lambda x: 1 if x else 0)

            embarked_encoded = self.enc.transform(passenger[['embarked']].values.reshape(-1, 1))
            passenger[self.encoded_cols] = embarked_encoded.toarray()
            passenger.drop(['embarked', 'name'], axis=1, inplace=True)

            dead_proba, alive_proba = np.squeeze(self.logreg.predict_proba(passenger))

            return {
                'Death probability': '{:.2%}'.format(dead_proba),
                'Survival probability': '{:.2%}'.format(alive_proba)
            }
        except Exception as e:
            return {'error': str(e)}


    def runDecisionTree(self):
        # more code here
        pass

    def runLogisticRegression(self):
        # more code here
        pass

    def predict_survival(self, passenger_data):
        # Method code here
        pass

# Initialize the Titanic model
def initTitanic():
    global titanic_regression
    titanic_regression = TitanicRegression()
    titanic_regression.initTitanic()

# Sample usage without API
if __name__ == "__main__":
    # Initialize the Titanic model
    initTitanic()
