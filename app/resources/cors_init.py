from flask_cors import CORS

cors = CORS()


def initialize_cors(app):
    cors.init_app(app)
