from flask import Flask
from flask_cors import CORS

from models import db

from Api_v1_0.api_blueprint import blueprint as blueprint_v1_0


def create_app(object_name):

    # init flask app
    app = Flask(__name__)

    # open the CORS
    CORS(app=app, supports_credentials=True)

    # config app
    app.config.from_object(object_name)

    # init database
    db.init_app(app)

    # register all blueprints in here
    app.register_blueprint(blueprint_v1_0, url_prefix='/api/v1')

    return app
