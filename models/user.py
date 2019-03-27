from app import app
from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property

# Import packages
import jwt
import datetime



class User(BaseModel):
    username=pw.CharField(unique=True)
    email=pw.CharField(unique=True)
    password=pw.CharField()
    profile_image = pw.CharField(null=True)

# Validation: user data

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append('Your username is not unique')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email and duplicate_email.id != self.id:
            self.errors.append('Your e-mail is not unique')

        if self.username=='':
            self.errors.append('You cannot enter a blank username')

        if self.email=='':
            self.errors.append('You cannot enter a blank username')

        
        


# Profile Image
    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return app.config['S3_LOCATION'] + self.profile_image
        else:
            return app.config['S3_LOCATION'] + "person-placeholder-image-3.jpg"

# RESTful: Update user data
    @hybrid_property
    def update_profile(self):


        return "pass"

# Login through apis (creating JWT) 

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 0
        except jwt.InvalidTokenError:
            return 0