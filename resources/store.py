import logging
import uuid
import json
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import stores, items
from flask import request


blp = Blueprint('stores', __name__, description = 'Operation on store')

@blp.route("/store/<string store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            # return {'message': 'Store not found'}, 404
            abort(404, message= 'Store not found')

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message='store not found')

class StoresList(MethodView):
    @blp.route('/stores')
    def get(self):
        # return {"hot reloading" : "no"}
        return {"stores" : list(stores.values())}

    @blp.route('/stores')  
    def post(self):
        req_json = request.get_data() # works ok
        req = json.loads(req_json)
        # return req['name']
        if 'name' not in req:
            abort(404, message = 'Bad request. "name" must be included in JSON payload.')
        for store in stores.values():
            if req['name'] == store['name']:
                abort(404, message = 'Bad request. store already exists.')
        storeId = uuid.uuid4().hex
        newStore = {**req, 'id' : storeId}
        stores[storeId] = newStore
        logging.info(req)
        # return {"stores" : stores} , 201
        return newStore, 201

# the blueprint way is a little awkward in my opinion, because it does not hold all related information in one class, 
# insted holds only those methods with exact same endpoint/route