from flask import Blueprint, jsonify, make_response, request
from models.user import User
from werkzeug.security import generate_password_hash


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

# RESTful - Read data
@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    # users = [(user.__dict__['__data__'] for user in users] # returns a full user object incl password!! (think of how you can exclude sensetive data from the returned JSON if you want to use this)
    users = [{"id": int(user.id), "username": user.username,
              "profileImage": user.profile_image_url} for user in users]
    return jsonify(users)

# RESTful - Create
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

# RESTful - Read data for EditProfile page
@users_api_blueprint.route('/me',methods=['GET'])

def show():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    user_id = User.decode_auth_token(auth_token)

    user = User.get_or_none(id=user_id)

    if user:
        responseObject={
            'username':user.username,
            'email':user.email
        }
   
        return jsonify(responseObject)
    else:
        responseObject = {
            'status': 'failed',
            'message': 'Authentication failed'
        }

        return make_response(jsonify(responseObject)), 401

# RESTful - Update profile
@users_api_blueprint.route('/edit',methods=['POST'])

def edit_profile():

    # Get JWT to verify which user has signed in
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        responseObject = {
            'status': 'failed',
            'message': 'No authorization header found'
        }

        return make_response(jsonify(responseObject)), 401

    # Locate the user ID based on the JWT token
    user_id = User.decode_auth_token(auth_token)
    # Grab the user object
    user = User.get_or_none(id=user_id)

    #Get JSON request
    post_data=request.get_json()

    if post_data['editPassword']:
        user.password=generate_password_hash(post_data['editPassword'])

    user.username=post_data['editUsername']
    user.email=post_data['editEmail']
    
    #Update in database

    if not user.save():

        responseObject = {
            'status': 'failed',
            'message': user.errors
        }

        return make_response(jsonify(responseObject)), 400

    else:
        
        responseObject = {
            'status': 'success',
            'message': 'Your profile has been successfully updated',
            'user': {"id": int(user.id),"username": user.username, "email": user.email}
        }

        return make_response(jsonify(responseObject)), 201

