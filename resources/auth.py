import datetime

from flask import request
from flask_jwt_extended import (
    create_access_token, get_raw_jwt,
    jwt_required)
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError

from database.models import User
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
from .jwt_init import jwt

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            user_id = user.id
            return {'id': str(user_id)}, 200
        except ValidationError as e:
            print("SignupApi ValidationError  : " + str(e))
            return {'error': str(e)}, 200
        except FieldDoesNotExist as e:
            print("SignupApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 200
        except NotUniqueError as e:
            print("SignupApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 200
        except Exception as e:
            print("SignupApi Exception  : " + str(e))
            return {'error': str(e)}, 200


class SocialAuthApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            if not (user is None):
                print("Value is not none user is already registered : " + str(user))
                expires = datetime.timedelta(days=365)
                access_token = create_access_token(identity=str(user.id), expires_delta=expires)
                return {'token': access_token, 'user_id': str(user.id)}, 200
        except User.DoesNotExist as e:
            print("Value is none user is not registered so registering and logging in : " + str(e))
            user = User(**body)
            user.hash_password()
            user.save()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token, 'user_id': str(user.id)}, 200
        except ValidationError as e:
            print("SocialAuthApi ValidationError  : " + str(e))
            return {'error': str(e)}, 200
        except FieldDoesNotExist as e:
            print("SocialAuthApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 200
        except NotUniqueError as e:
            print("SocialAuthApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 200
        except Exception as e:
            print("SocialAuthApi Exception  : " + str(e))
            return {'error': str(e)}, 200


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token, 'user_id': str(user.id)}, 200
        except (UnauthorizedError, DoesNotExist) as e:
            print("LoginApi Unauthorised  : " + str(e))
            return {'error': str(e)}, 200
        except ValidationError as e:
            print("LoginApi ValidationError  : " + str(e))
            return {'error': str(e)}, 200
        except FieldDoesNotExist as e:
            print("LoginApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 200
        except NotUniqueError  as e:
            print("LoginApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 200
        except Exception as e:
            print("LoginApi Exception  : " + str(e))
            return {'error': str(e)}, 200


class LogoutApi(Resource):
    @jwt_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            return {'msg': 'Logged out successfully'}, 200
        except Exception as e:
            print("SignupApi Exception  : " + str(e))
            return {'error': str(e)}, 200
