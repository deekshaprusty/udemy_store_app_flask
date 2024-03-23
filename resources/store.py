import logging
import uuid
import json
from flask_smorest import Blueprint, abort
from flask.views import MethodView
# from db import stores, items
from flask import request
from schemas import StoreSchema
from models import StoreModel
from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint('stores', __name__, description = 'Operation on store')

@blp.route('/stores/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented")

@blp.route('/stores')
class StoresList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"hot reloading" : "no"}
        # return {"stores" : list(stores.values())}
        # return stores.values()
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, req):
        newStore = StoreModel(**req)
        try:
            db.session.add(newStore)
            db.session.commit()
        except IntegrityError :
            abort(400, message ="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message = 'An error occurred while inserting the item')
        
        return newStore, 201


# the blueprint way is a little awkward in my opinion, because it does not hold all related information in one class, 
# insted holds only those methods with exact same endpoint/route