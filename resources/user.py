
import sys
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from passlib.hash import pbkdf2_sha256
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import UserSchema
from flask_jwt_extended import create_access_token

bp = Blueprint("Users", "Users", description = "operations on user")

@bp.route("/register")
class User(MethodView):

    @bp.arguments(UserSchema)
    # @bp.response(UserSchema)
    def post(self, userdata):
        usr = UserModel(username=userdata["username"], pswd = pbkdf2_sha256.hash(userdata["pswd"])) 
        try:
            db.session.add(usr)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500 , message=str(ex))
        return {'message':'user successfully created'}, 201

@bp.route('/users/<string:username>')
class GetDeleteUser(MethodView):

    # @bp.arguments
    @bp.response(200, UserSchema(many=True))
    def get(self, username):
        print(f'username : {username}')
        sys.stdout.flush()
        usr = UserModel.query.filter(UserModel.username==username)
        return usr
        

    @bp.response(200, UserSchema)
    def delete(self, username):
        usr = UserModel.query.filter(UserModel.username == username).first()
        try:
            db.session.delete(usr)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500, message='error while deleting')
        return usr


@bp.route("/login")
class UserLogin(MethodView):

    @bp.arguments(UserSchema)
    def post(self, userdata):
        usr = UserModel.query.filter(UserModel.username == userdata["username"]).first()
        if usr:
            if pbkdf2_sha256.verify(userdata["pswd"], usr.pswd):  # this order is important obviously, it is not just == operator
                access_token = create_access_token(identity = usr.id)
                return {"access_token" : access_token}
        abort(401, message="invalid credentials")






