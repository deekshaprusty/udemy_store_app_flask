from db import items
from flask import request
from flask.views import MethodView   
from flask_smorest import Blueprint, abort
import uuid
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', __name__, description = 'Operations on items')

@blp.route('/items/<string:item_id>')
class Item(MethodView):    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            # return {'message' : 'item not found'},404
            abort(404, message = 'item not found')

    def delete(self, itemid):
        try:
            items.pop(itemid)
            return {'message' : 'itemid deleted'}
        except KeyError:
            abort(404, message='item not found')

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, updatedItem, item_id):
        # updatedItem = request.get_json()
        # if 'price' not in updatedItem or 'name' not in updatedItem:
            # abort(400, message = 'bad request, Ensure price and name in the JSON payload.')
        # item = items[item_id]
        try:
            items[item_id]= updatedItem
            return {'message' : 'item_updated', 'items' : items}
        except:
            abort(404, message = 'item not found' )

@blp.route('/item')
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return list(items.values() )
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, itemInfo):
        # itemInfo = request.get_json()
        # if 'store_id' not in itemInfo or 'price' not in itemInfo or 'name' not in itemInfo:
        #     abort(400, message = 'bad request. Ensure store_id, price, name are included in JSON payload')
        for item in items.values():
            if itemInfo['name'] == item['name'] and itemInfo['store_id'] == item['store_id']:
                abort(404, message='Item already exists')

        # storeId = itemInfo.get('store_id')
        # if storeId not in stores:
        #     return {'message': 'store not found'}, 404

        itemId = itemId = uuid.uuid4().hex
        newItem= {**itemInfo, 'id' : itemId}
        items[itemId] = newItem
        return newItem, 201