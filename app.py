from flask import Flask
from flask_bcrypt import Bcrypt

from flask_mail import Mail

from database.db import initialize_db
from flask_restful import Api
from resources.errors import errors
from resources.jwt_init import initialize_jwt

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# app.config['JWT_TOKEN_LOCATION'] = ['json']
mail = Mail(app)

# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)

initialize_jwt(app)
initialize_db(app)
initialize_routes(api)
