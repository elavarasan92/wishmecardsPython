from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from database.models import VisitingCard, User


class VisitingCardsApi(Resource):
    @jwt_required
    def get(self):
        query = VisitingCard.objects()
        visiting_cards = VisitingCard.objects().to_json()
        return Response(visiting_cards, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            print("user_id : " + str(user_id))
            body = request.get_json()
            print("body : " + str(request.get_json()))
            user = User.objects.get(id=user_id)
            visiting_card = VisitingCard(**body, added_by=user)
            visiting_card.save()
            user.update(push__visiting_card=visiting_card)
            user.save()
            event_id = visiting_card.id
            return {'id': str(event_id)}, 200
        except ValidationError as e:
            print("VisitingCardApi ValidationError  : " + str(e))
            return {'error': str(e)}, 200
        except FieldDoesNotExist as e:
            print("VisitingCardApi FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 200
        except NotUniqueError as e:
            print("VisitingCardApi NotUniqueError  : " + str(e))
            return {'error': str(e)}, 200
        except Exception as e:
            print("VisitingCardApi Exception  : " + str(e))
            return {'error': str(e)}, 200


class VisitingCardApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            visiting_card = VisitingCard.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            VisitingCard.objects.get(id=id).update(**body)
            return {'id': str(id)+" : Successfully Updated"}, 200
        except InvalidQueryError as e:
            return {'error': str(e)}, 200
        except DoesNotExist as e:
            return {'error': str(e)}, 200
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

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            visiting_card = VisitingCard.objects.get(id=id, added_by=user_id)
            visiting_card.delete()
            return {'id': str(id)+" : Successfully Deleted"}, 200
        except DoesNotExist as e:
            return {'error': str(e)}, 200
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

    def get(self, id):
        try:
            visiting_cards = VisitingCard.objects.get(id=id).to_json()
            return Response(visiting_cards, mimetype="application/json", status=200)
        except DoesNotExist as e:
            return {'error': str(e)}, 200
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
