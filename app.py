import os

from flask import Flask, request
from flask_smorest import abort, Api
import logging
import uuid
import json
# from db import stores, items
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
import models
from db import db



# stores = [
#     {"name" : "Tambi Stores",
#     "items" : [
#         {"name" : "chair",
#         "price" : 9.5
#         }
#     ]
#     },
# ]
def create_app(db_url = None):
    app = Flask(__name__)
    logging.info('Flask started :::::::::::::::')
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"  #OPENAPI is a standard for API documentation. Here we tell smorest to use which version to use for documentation
    app.config["OPENAPI_URL_PREFIX"] = "/"  #here we tell smorest where root of the URL is? WHat does it mean exactly? Perhaps Change the value to find out.
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv( "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    try:
        db.init_app(app)
    except Exception as ex:
        print(f'type of db - {type(db)}')
        print('dir(db)')
        print(dir(db))
        raise ex
    api = Api(app)

    # @app.before_first_request
    # def create_tables():
    with app.app_context():
        db.create_all()


    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    app.debug = True
    return app


create_app()
# @app.post('/store')
# def create_store():
#     req_json = request.get_json()
#     stores.append(req_json)
#     return req_json, 201



# the below is not required. flask run takes settings from .flaskenv (also with that, we no longer need to start the server with each change. it gets updated automatically)
# #Has not worked - the below would be required if you are debugging
# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)

# running instruction

# vscode settings - make sure the correst folder is added as one of the workspaces

#install requirements

# navigate to udemy_store folder
# python -m venv venv
# Set-ExecutionPolicy Unrestricted -Scope Process
# venv\Scripts\activate
# 
# # pip install -r requirements.txt
# flask run


# Docker volume - hot reloading (the below is not working. needs work)
# docker run -p 8080:5000 -w /app -v "C:\Users\prust\OneDrive\Documents\Deeksha\Flask_Projects\udemy_store:\app" flask-smorest-api

