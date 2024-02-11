from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS
import requests  # used for testing 
import random
import os

from model.memeforge_functions import *
from model.memeforge_database import *


meme_forge_api = Blueprint('meme_forge_api', __name__,
                   url_prefix='/api/memeforge')

api = Api(meme_forge_api)
# CORS(meme_forge_api, resources={r"/api/*": {"origins": "*"}})
class MemeForgeAPI:

    class _Maker(Resource):
        def post(self):
            data = request.get_json()
            combined_image = combine(data['base64image1'], data['base64image2'], data['direction'])
            response = jsonify({"base64image": combined_image})
            if data['addToHistory']:
                createImage(data['filename'], 'combine', combined_image) # adds to database
            return response
        
    class _GetDatabase(Resource):
        def get(self):
            return queryImages()
        
    class _AddImage(Resource):
        def post(self):
            data = request.get_json()
            createImage(data["Name"], data["Function"], data["Base64Image"])
            
    class _ClearDatabase(Resource):
        def get(self):
            clearDatabase()



    api.add_resource(_Maker, '/maker/')
    api.add_resource(_GetDatabase, '/get_database')
    api.add_resource(_AddImage, '/add_image')
    api.add_resource(_ClearDatabase, '/clear_database')