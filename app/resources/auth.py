import datetime

from flask import Response, request
from flask_jwt_extended import (
    create_access_token, get_raw_jwt,
    jwt_required)
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from werkzeug.exceptions import InternalServerError

from app.database.models import User
from app.resources.errors import UnauthorizedError, SchemaValidationError, UpdatingMovieError, DeletingMovieError, \
    MovieNotExistsError
from .jwt_init import jwt

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


class UsersApi(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)


class UserApi(Resource):

    def get(self, id):
        try:
            user = User.objects.get(email=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            print("user doesnt exist")
            return 'user doesnt exist', 404
        except Exception:
            raise InternalServerError

    @jwt_required
    def put(self, id):
        try:
            print("Put email id : user : " + id)
            body = request.get_json()
            User.objects.get(email=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return 'deleted successfully', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(body)
            user.hash_password()
            user.save()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            user.access_token = access_token
            user_json = user.to_json()
            return Response(user_json, mimetype="application/json", status=200)
        except ValidationError as e:
            print("SignupApi ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("SignupApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("SignupApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 409
        except Exception as e:
            print("SignupApi Exception  : " + str(e))
            return {'error': str(e)}, 500


class SocialAuthApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            if not (user is None):
                print("Value is not none user is already registered : " + str(user))
                expires = datetime.timedelta(days=365)
                access_token = create_access_token(identity=str(user.id), expires_delta=expires)
                user.access_token = access_token
                if user.visiting_card_exist:
                    user.visiting_card_id = user.visiting_card.id
                return Response(user.to_json(), mimetype="application/json", status=200)
        except User.DoesNotExist as e:
            print("Value is none user is not registered so registering and logging in : " + str(e))
            user = User(**body)
            user.hash_password()
            user.save()
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            user.access_token = access_token
            if user.visiting_card_exist:
                user.visiting_card_id = user.visiting_card.id
            return Response(user.to_json(), mimetype="application/json", status=200)
        except ValidationError as e:
            print("SocialAuthApi ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("SocialAuthApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("SocialAuthApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("SocialAuthApi Exception  : " + str(e))
            return {'error': str(e)}, 500


class LoginApi(Resource):
    def post(self):
        try:
            print("request: " + str(request))
            body = request.get_json()
            print("Body: " + str(body))
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            user.access_token = access_token
            if user.visiting_card_exist:
                user.visiting_card_id = user.visiting_card.id
            return Response(user.to_json(), mimetype="application/json", status=200)
        except (UnauthorizedError, DoesNotExist) as e:
            print("LoginApi Unauthorised  : " + str(e))
            return {'error': str(e)}, 401
        except ValidationError as e:
            print("LoginApi ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("LoginApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("LoginApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("LoginApi Exception  : " + str(e))
            return {'error': str(e)}, 500


class LogoutApi(Resource):
    @jwt_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            return {'msg': 'Logged out successfully'}, 200
        except Exception as e:
            print("SignupApi Exception  : " + str(e))
            return {'error': str(e)}, 500
