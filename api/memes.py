import json
from flask import Blueprint, request, jsonify
import requests
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

memes_api = Blueprint('memes_api', __name__,
                   url_prefix='/api/memes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(memes_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def get(self, ingredients): # Create method
            api_key = '84cfe45628de456c87a13a80b76f5bd8'  # Replace with your Spoonacular API key
            url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients=" + ingredients
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return jsonify(data)
            else:
                #return jsonify({"error": "Failed to fetch recipes."}), response.status_code
             return {'message': f'hello'}, 400
        
    
    #api.add_resource(_CRUD, '/getrecipes/<ingredients>')