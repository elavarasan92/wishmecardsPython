from flask import Response, request, render_template, jsonify, make_response
from flask_restful import Resource


class BusinessCardApi(Resource):
    def get(self, id):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', id=id), 200, headers)


class RenderHTMLApi(Resource):
    # to get html for uploading image
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('render_html.html'), 200, headers)
