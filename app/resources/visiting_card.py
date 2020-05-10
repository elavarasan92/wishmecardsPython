from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from app.database.models import VisitingCard, User


class VisitingCardsApi(Resource):
    @jwt_required
    def get(self):
        try:
            query = VisitingCard.objects()
            visiting_cards = VisitingCard.objects().to_json()
            return Response(visiting_cards, mimetype="application/json", status=200)
        except Exception as e:
            print("VisitingCardApi  get all cards Exception  : " + str(e))
            return {'error': str(e)}, 500


    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            print("user_id : " + str(user_id))
            body = request.get_json()
            print("body : " + str(request.get_json()))
            user = User.objects.get(id=user_id)
            visiting_card = VisitingCard.objects.get(added_by=user_id)
            print(visiting_card.id)
            if not (visiting_card is None):
                print("visiting card exist ")
                return Response(visiting_card.to_json(), mimetype="application/json", status=200)
        except DoesNotExist as e:
            print("VisitingCardApi post DoesNotExist since no visiting card exist for this user creating new one : " + str(e))
            visiting_card = VisitingCard(**body, added_by=user)
            visiting_card.save()
            user.update(visiting_card=visiting_card)
            user.visiting_card_exist = True
            user.save()
            print("visiting_card  : " + visiting_card.to_json())
            return Response(visiting_card.to_json(), mimetype="application/json", status=200)
        except ValidationError as e:
            print("VisitingCardApi post ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("VisitingCardApi post FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("VisitingCardApi post NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("VisitingCardApi post Exception  : " + str(e))
            return {'error': str(e)}, 500


class VisitingCardApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            visiting_card = VisitingCard.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            VisitingCard.objects.get(id=id).update(**body)
            print("visiting_card  : " + visiting_card.to_json())
            return Response(visiting_card.to_json(), mimetype="application/json", status=200)
        except InvalidQueryError as e:
            print("VisitingCardApi put InvalidQueryError  : " + str(e))
            return {'error': str(e)}, 200
        except DoesNotExist as e:
            print("VisitingCardApi put DoesNotExistError  : " + str(e))
            return {'error': str(e)}, 400
        except ValidationError as e:
            print("VisitingCardApi put ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("VisitingCardApi put FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("VisitingCardApi put NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("VisitingCardApi put Exception  : " + str(e))
            return {'error': str(e)}, 500

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            visiting_card = VisitingCard.objects.get(id=id, added_by=user_id)
            visiting_card.delete()
            return {'id': str(id)+" : Successfully Deleted"}, 200
        except DoesNotExist as e:
            print("VisitingCardApi delete DoesNotExistError  : " + str(e))
            return {'error': str(e)}, 400
        except ValidationError as e:
            print("VisitingCardApi delete ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("VisitingCardApi delete FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("VisitingCardApi delete NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("VisitingCardApi delete Exception  : " + str(e))
            return {'error': str(e)}, 500

    @jwt_required
    def get(self, id):
        try:
            print("id: "+str(id))
            user_id = get_jwt_identity()
            print("userid : "+user_id)
            visiting_card = VisitingCard.objects.get(id=id, added_by=user_id).to_json()
            print("visiting card get by id : "+visiting_card)
            return Response(visiting_card, mimetype="application/json", status=200)
        except DoesNotExist as e:
            print("VisitingCardApi get single card by id  DoesNotExistError  : " + str(e))
            return {'error': str(e)}, 400
        except ValidationError as e:
            print("VisitingCardApi get single card by id ValidationError  : " + str(e))
            return {'error': str(e)}, 400
        except FieldDoesNotExist as e:
            print("VisitingCardApi get single card by id FieldDoesNotExist  : " + str(e))
            return {'error': str(e)}, 400
        except NotUniqueError as e:
            print("VisitingCardApi get single card by id NotUniqueError  : " + str(e))
            return {'error': str(e)}, 400
        except Exception as e:
            print("VisitingCardApi get single card by id Exception  : " + str(e))
            return {'error': str(e)}, 5
