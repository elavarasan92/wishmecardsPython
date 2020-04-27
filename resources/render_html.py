from flask import Response, request, render_template, jsonify, make_response
from flask_restful import Resource


class RenderHTMLApi(Resource):
    # to get html for uploading image
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('render_html.html'), 200, headers)