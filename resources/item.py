# from db import items
from flask import request
from flask.views import MethodView   
from flask_smorest import Blueprint, abort
import uuid
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
import logging
import sys
from flask_jwt_extended import jwt_required

blp = Blueprint('items', __name__, description = 'Operations on items')

@blp.route('/items/<string:item_id>')
class Item(MethodView):    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
            logging.info("Debugging ::::: Item.get called")
            print(f'Debugging ::::: Item.get called - print')
            sys.stdout.flush()
            item = ItemModel.query.get_or_404(item_id)
            return item

    @jwt_required()
    @blp.response(200, ItemSchema)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
        return {"message" : "item deleted"}
        # raise NotImplementedError("Deleting an item is not implemented")

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, updatedItem, item_id):
        # updatedItem = request.get_json()
        # if 'price' not in updatedItem or 'name' not in updatedItem:
            # abort(400, message = 'bad request, Ensure price and name in the JSON payload.')
        # item = items[item_id]
        print(f' updatedItem : {updatedItem}')
        sys.stdout.flush()
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = updatedItem['price']
            item.name = updatedItem['name']
            item.store_id = updatedItem['store_id']
        else:
            item = ItemModel(id = item_id, **updatedItem)
        print(f' store id of item obj : {item.store_id}')
        
        
        sys.stdout.flush()
        db.session.add(item)
        db.session.commit()
        return item
        # raise NotImplementedError("Updating an item is not implemented")

@blp.route('/item')
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return list(items.values() )
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, itemInfo):
        # itemInfo = request.get_json()
        # if 'store_id' not in itemInfo or 'price' not in itemInfo or 'name' not in itemInfo:
        #     abort(400, message = 'bad request. Ensure store_id, price, name are included in JSON payload')


        # storeId = itemInfo.get('store_id')
        # if storeId not in stores:
        #     return {'message': 'store not found'}, 404
        logging.info(f' itemInfo - {itemInfo}')
        print(f' itemInfo : {itemInfo}')
        sys.stdout.flush()        
        newItem = ItemModel(**itemInfo)
        try:
            db.session.add(newItem)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting the item')

        return newItem, 201


#Introducing Tags
#1. accept a tag_name field in Item.
#2. Create a tag 

#2. Create a tag 
# Tag Model 
#     id - dump_only
#     tag_name
#     store -> back populates similar to 1-M
#     item - dont accept while creating a tag

# Store Model
# Add Item as back populates -> 1-M

# # Tag Schema
#     id - dump_only
#     tag_name
#     store
#     item - dont accept while creating a tag

# #1. accept a tag_name field in Item.
# change to Item Schema

# # Overall
# 1 Store -> M Tags
# M Tags -> M Items

# Tag_Item Model












