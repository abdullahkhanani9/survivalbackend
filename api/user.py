import json
from flask import Blueprint, request, jsonify,  make_response
from flask_restful import Api, Resource # used for REST API building
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from flask_cors import CORS

from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

CORS(user_api)

class UserAPI:        
    class _CRUD(Resource): 
        def post(self): 
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      uid=uid, password=password)
            
            ''' Additional garbage error checking '''
            if password is not None:
                uo.set_password(password)
                
            ''' #2: Key Code block to add user to database '''
            user = uo.create()
            if user:
                return user.read()
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): 
            users = User.query.all()    
            json_ready = [user.read() for user in users]  
            return (json_ready) 

    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            name = body.get('name')
            uid = body.get('uid')
            password = body.get('password')
            if uid is not None:
                new_user = User(name=name, uid=uid, password=password)
            user = new_user.create()
            if user:
                return user.read()
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            login_user(user)
            return jsonify(user.read())
        
    class Login(Resource):
        def post(self):
            data = request.get_json()

            uid = data.get('uid')
            password = data.get('password')

            if not uid or not password:
                response = {'message': 'Invalid creds'}
                return make_response(jsonify(response), 401)

            user = User.query.filter_by(_uid=uid).first()

            if user and user.is_password(password):
         
                response = {
                    'message': 'Logged in successfully',
                    'user': {
                        'name': user.name,  
                        'id': user.id
                    }
                }
                return make_response(jsonify(response), 200)

            response = {'message': 'Invalid id or pass'}
            return make_response(jsonify(response), 401)



    class Logout(Resource):
        @login_required
        def post(self):
            logout_user()
            return {'message': 'Logged out successfully'}, 200
            
   

                 

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(_Create, '/create')
    
    
    
    