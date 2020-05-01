#src/app.py

from flask import Flask, request, json, Response, Blueprint
from .config import app_config
from .models import db
from ..models.CharacterModel import CharacterModel
from ..models.HatModel import HatModel

def create_app(env_name):
    """
    Create app
    """
    
    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    db.init_app(app)

    # Create an user
    @app.route('/', methods=['POST'])
    def create():
        """
        Create User Function
        """
        req_data = request.get_json()
        data, error = user_schema.load(req_data)

        if error:
            return custom_response(error, 400)
        
        # check if user already exist in the db
        user_in_db = UserModel.get_user_by_email(data.get('email'))
        if user_in_db:
            message = {'error': 'User already exist, please supply another email address'}
            return custom_response(message, 400)
        
        user = UserModel(data)
        user.save()

        ser_data = user_schema.dump(user).data

        token = Auth.generate_token(ser_data.get('id'))

        return custom_response({'jwt_token': token}, 201)

    # Get all Characters
    @app.route('/character/', methods=['GET'])
    def get_all_char():
        users = CharacterModel.get_all_users()
        #ser_users = user_schema.dump(users, many=True).data
        return custom_response(ser_users, 200)  

    # Get all Characters
    @app.route('/hat/', methods=['GET'])
    def get_all_hat():
        users = HatModel.get_all_users()
        ser_users = user_schema.dump(users, many=True).data
        return custom_response(ser_users, 200)  

    # Get an user
    @app.route('/<int:id>', methods=['GET'])
    def get_a_user(user_id):
        """
        Get a single user
        """
        character = Character.query.get(id)
        if not Character:
            return custom_response({'error': 'user not found'}, 404)
        
        ser_user = user_schema.dump(user).data
        return custom_response(ser_user, 200)

    # Update an user
    @app.route('/<int:user_id>', methods=['PUT'])
    def update():
        """
        Update me
        """
        req_data = request.get_json()
        data, error = user_schema.load(req_data, partial=True)
        if error:
            return custom_response(error, 400)

        user = UserModel.get_one_user(g.user.get('id'))
        user.update(data)
        ser_user = user_schema.dump(user).data
        return custom_response(ser_user, 200)

    # Delete an user
    @app.route('/<int:user_id>', methods=['DELETE'])
    def delete():
        """
        Delete a user
        """
        user = UserModel.get_one_user(g.user.get('id'))
        user.delete()
        return custom_response({'message': 'deleted'}, 204)

    def custom_response(res, status_code):
        """
        Custom Response Function
        """
        return Response(
            mimetype="application/json",
            response=json.dumps(res),
            status=status_code
        )

    return app