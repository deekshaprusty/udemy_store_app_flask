from db import items
from flask import request
from flask_smorest import Blueprint, abort


blp = Blueprint('items', __name__, description = 'Operations on items')




@blp.route('/items/<string:item_id>')
def get(self, item_id):
    try:
        return items[item_id]
    except KeyError:
        # return {'message' : 'item not found'},404
        abort(404, message = 'item not found')

@blp.route('/items/<string:itemid>')
def delete(self, itemid):
    try:
        items.pop(itemid)
        return {'message' : 'itemid deleted'}
    except KeyError:
        abort(404, message='item not found')

@blp.route('/items/<string:item_id>')
def put(self, item_id):
    updatedItem = request.get_json()
    if 'price' not in updatedItem or 'name' not in updatedItem:
        abort(400, message = 'bad request, Ensure price and name in the JSON payload.')
    # item = items[item_id]
    try:
        items[item_id]= updatedItem
        return {'message' : 'item_updated', 'items' : items}
    except:
        abort(404, message = 'item not found' )
