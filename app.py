from flask import Flask, request
from flask_smorest import abort
import logging
import uuid
import json
from db import stores, items


app = Flask(__name__)


# stores = [
#     {"name" : "Tambi Stores",
#     "items" : [
#         {"name" : "chair",
#         "price" : 9.5
#         }
#     ]
#     },
# ]

@app.get('/stores')
def get_stores():
    # return {"hot reloading" : "no"}
    return {"stores" : list(stores.values())}

@app.post('/stores')  
def create_store():
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

@app.get('/stores/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        # return {'message': 'Store not found'}, 404
        abort(404, message= 'Store not found')

@app.post('/item')
def create_item():
    itemInfo = request.get_json()
    if 'store_id' not in itemInfo or 'price' not in itemInfo or 'name' not in itemInfo:
        abort(400, message = 'bad request. Ensure store_id, price, name are included in JSON payload')
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

@app.get('/items/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        # return {'message' : 'item not found'},404
        abort(404, message = 'item not found')

@app.delete('/items/<string:itemid>')
def deleteItem(itemid):
    try:
        items.pop(itemid)
        return {'message' : 'itemid deleted'}
    except KeyError:
        abort(404, message='item not found')

@app.put('/items/<string:item_id>')
def updateItem(item_id):
    updatedItem = request.get_json()
    if 'price' not in updatedItem or 'name' not in updatedItem:
        abort(400, message = 'bad request, Ensure price and name in the JSON payload.')
    # item = items[item_id]
    try:
        items[item_id]= updatedItem
        return {'message' : 'item_updated', 'items' : items}
    except:
        abort(404, message = 'item not found' )


@app.get('/items')
def get_all_items():
    return list(items.values() )
    

@app.delete('/stores/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message='store not found')


# @app.post('/store')
# def create_store():
#     req_json = request.get_json()
#     stores.append(req_json)
#     return req_json, 201



# the below is not required. flask run takes settings from .flaskenv (also with that, we no longer need to start the server with each change. it gets updated automatically)
# if __name__ == "__main__":
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