from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
from flask_cors import CORS
import requests  # used for testing 
import random
import os
from auth_middleware import token_required
from model.memeforge_functions import *
from model.memeforge_database import *
from flask_login import login_user, logout_user, current_user, login_required

meme_forge_api = Blueprint('meme_forge_api', __name__,
                   url_prefix='/api/memeforge')

api = Api(meme_forge_api)

class MemeForgeAPI:

    class _MemeMaker(Resource):
        def post(self):
            data = request.get_json()
            base64_image = data['base64data']
            top_text = data['top_text']
            bottom_text = data['bottom_text']

            meme_image = meme_maker(base64toImage(base64_image), top_text, bottom_text)

            response = jsonify({"base64image": imageToBase64(meme_image)})

            if data['addToHistory']:
                createImage(data['filename'], 'meme', imageToBase64(meme_image))

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



    api.add_resource(_MemeMaker, '/maker/')
    api.add_resource(_GetDatabase, '/get_database')
    api.add_resource(_AddImage, '/add_image')
    api.add_resource(_ClearDatabase, '/clear_database')