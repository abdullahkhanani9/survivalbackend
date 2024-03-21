from flask import Flask, request, jsonify
from flask import Blueprint
from flask_restful import Api, Resource
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import numpy as np
import pickle
titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')
api = Api(titanic_api)

class TitanicAPI(Resource):
    def __init__(self):
        titanic_data = sns.load_dataset('titanic')
        td = titanic_data.copy()
        td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
        td.dropna(inplace=True)
        td['sex'] = td['sex'].apply(lambda x: 1 if x == 'male' else 0)
        td['alone'] = td['alone'].apply(lambda x: 1 if x else 0)

        self.enc = OneHotEncoder(handle_unknown='ignore')
        embarked_encoded = self.enc.fit_transform(td[['embarked']].values.reshape(-1, 1))
        self.encoded_cols = self.enc.get_feature_names_out(['embarked'])

        td[self.encoded_cols] = embarked_encoded.toarray()
        td.drop(['embarked'], axis=1, inplace=True)
        self.logreg = LogisticRegression(max_iter=1000)
        X = td.drop('survived', axis=1)
        y = td['survived']
        self.logreg.fit(X, y)
        

    

    def post(self):
        try:
            data = request.get_json()
            pclass=data.get('pclass')
            sex=data.get('sex')
            age=data.get('age')
            fare=data.get('fare')
            embarked=data.get('embarked')
            sibsp=data.get('sibsp')
            parch=data.get('parch')
            alone=data.get('alone')
            passthrough=[int(i) for i in [pclass,sex,age,fare,embarked,sibsp,parch,alone]]
            print(passthrough)
            result = self.logreg.predict([passthrough])
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

api.add_resource(TitanicAPI, '/predict')