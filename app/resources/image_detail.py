import io

import werkzeug
from flask import Response, request, render_template, jsonify, make_response
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, Api, reqparse
from mongoengine.errors import DoesNotExist, InvalidQueryError
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from app.database.models import ImageDetail, VisitingCard
from app.resources.errors import SchemaValidationError, InternalServerError, \
    UpdatingImageDetailError, DeletingImageDetailError, ImageDetailNotExistsError

parser = reqparse.RequestParser()
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
errors = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class DisplayImageApi(Resource):
    def get(self,id):
        image_value = ImageDetail.objects(image_ref_id=id).first()
        photo = image_value.image_data.read()
        content_type = image_value.image_data.content_type
        print(photo)
        print(content_type)
        return send_file(io.BytesIO(photo), attachment_filename='profile.png', mimetype='image/png')


class UploadImageApi(Resource):
    def post(self,id):
        print("Visiting card id to upload image to  that : "+id)
        visiting_card_id = id
        try:
            data = parser.parse_args()
            print(data);
            print(data['file'])
            if data['file'] is None or data['file'] == "":
                return {
                    'data': '',
                    'message': 'No file found',
                    'status': 'error'
                }
            photo = data['file']

            if photo:
                if photo and allowed_file(photo.filename):
                    filename = secure_filename(photo.filename)
                    couple_image = ImageDetail.objects.get(image_ref_id=visiting_card_id)
                    if not (couple_image is None):
                        print("Image already exist updating " + str(couple_image))
                        couple_image.image_data.new_file()
                        couple_image.image_data.replace(photo, filename="image.jpg")
                        couple_image.image_data.close()
                        couple_image.save()
                        visiting_card = VisitingCard.objects.get(id=visiting_card_id)
                        print(visiting_card.id)
                        if not (visiting_card is None):
                            print("visiting card exist ")
                            print("File uploaded successfully ")
                            visiting_card.update(profile_picture_exist=True)
                            visiting_card.save()
                            return {
                                'data': '',
                                'message': 'photo uploaded',
                                'status': 'success'
                            }
                        else:
                            print("visiting card doesnt  exist ")
                            return {
                                'data': 'visiting card doesnt exist with id '+visiting_card_id,
                                'message': 'photo upload failed',
                                'status': 'errror'
                            }
                else:
                    errors[photo.filename] = 'File type is not allowed'
                    print("File upload  Failed ")
                    return {
                        'data': 'visiting card doesnt exist with id '+visiting_card_id,
                        'message': 'photo upload failed',
                        'status': 'errror'
                    }
        except DoesNotExist:
            print("Image doesnt exist saving ")
            couple_image1 = ImageDetail(image_ref_id=visiting_card_id)
            couple_image1.image_data.new_file()
            couple_image1.image_data.replace(photo, filename="image.jpg")
            couple_image1.image_data.close()
            couple_image1.save()
            print("File uploaded successfully ")
            visiting_card = VisitingCard.objects.get(id=visiting_card_id)
            print(visiting_card.id)
            if not (visiting_card is None):
                print("visiting card exist ")
                print("File uploaded successfully ")
                visiting_card.update(profile_picture_exist=True)
                visiting_card.save()
                return {
                    'data': '',
                    'message': 'photo uploaded',
                    'status': 'success'
                }
            else:
                print("visiting card doesnt  exist ")
                return {
                    'data': 'visiting card doesnt exist with id ' + visiting_card_id,
                    'message': 'photo upload failed',
                    'status': 'errror'
                }
        except Exception as e:
            print("File upload exception  : " + str(e))
            return {
                'data': str(e) + visiting_card_id,
                'message': 'photo upload failed',
                'status': 'errror'
            }
