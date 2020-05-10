import io
from flask import Response, request, render_template, jsonify, make_response
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, InvalidQueryError
from werkzeug.utils import secure_filename

from app.database.models import ImageDetail
from app.resources.errors import SchemaValidationError, InternalServerError, \
    UpdatingImageDetailError, DeletingImageDetailError, ImageDetailNotExistsError

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#http://127.0.0.1:3500/display_image/5e9327491848788505e send object id that is id of user or eventdetail object
class DisplayImageApi(Resource):
    def get(self,id):
        image_value = ImageDetail.objects(image_ref_id=id).first()
        photo = image_value.image_data.read()
        content_type = image_value.image_data.content_type
        print(photo)
        print(content_type)
        return send_file(io.BytesIO(photo), attachment_filename='profile.png', mimetype='image/png')


class UploadImageApi(Resource):
    # to get html for uploading image
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('file-upload.html'), 200, headers)

    # to upload file
    def post(self):
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        #image_ref_id = request.image_ref_id
        # pretty printing data
        print("Form : "+str(request.form.get('image_ref_id')))
        print("get_json : " + str(request.get_json()))

        files = request.files.getlist('files[]')
        image_ref_id = request.form.get('image_ref_id')
        errors = {}
        success = False

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                couple_image = ImageDetail(image_ref_id=image_ref_id)
                couple_image.image_data.new_file()
                couple_image.image_data.replace(file, filename="image.jpg")
                couple_image.image_data.close()
                couple_image.save()

                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 206
            return resp
        if success:
            resp = jsonify({'message': 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            print(errors)
            resp = jsonify(errors)
            resp.status_code = 400
            print(resp)
            return resp


class EditImageApi(Resource):
    @jwt_required
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            couple_image = ImageDetail.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            ImageDetail.objects.get(id=id).update(**body)
            return 'Successfully updated image ', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingImageDetailError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            couple_image = ImageDetail.objects.get(id=id, added_by=user_id)
            couple_image.delete()
            return 'Successfully deleted Image', 200
        except DoesNotExist:
            raise DeletingImageDetailError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            couple_images = ImageDetail.objects.get(id=id).to_json()
            return Response(couple_images, mimetype="application/json", status=200)
        except DoesNotExist:
            raise ImageDetailNotExistsError
        except Exception:
            raise InternalServerError
