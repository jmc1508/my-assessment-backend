from flask import Blueprint, jsonify, make_response, request
from models.user import User
from werkzeug.security import generate_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/',methods=['POST'])
def create():

    # get the post data
    post_data=request.get_json()

    try:
        new_user = User(
            username=post_data['username'],
            email=post_data['email'].lower(),
            password=generate_password_hash(post_data['password'])
        )

    

    except:
        responseObject = {
            'status': 'failed',
            'message': ['All fields are required!']
        }

        return make_response(jsonify(responseObject)), 400

    else:

        if not new_user.save():

            responseObject = {
                'status': 'failed',
                'message': new_user.errors
            }

            return make_response(jsonify(responseObject)), 400

        else:
            
            auth_token = new_user.encode_auth_token(new_user.id)

            responseObject = {
                'status': 'success',
                'message': 'Successfully created a user and signed in.',
                'auth_token': auth_token.decode(),
                'user': {"id": int(new_user.id), "username": new_user.username, "profile_picture": new_user.profile_image_url}
            }

            return make_response(jsonify(responseObject)), 201

