from marshmallow import Schema, fields
import sys


class PlainItemSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required=True)
    price = fields.Float(required = True)
    
    

class ItemUpdateSchema(Schema):
    print(f'Debugging : ItemUpdateSchema ')
    sys.stdout.flush()    
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    id = fields.Str()

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required=True)
    
    
class PlainTagSchema(Schema):
    id = fields.Integer(dump_only = True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Integer(required= True)
    # tag_ids = fields.Integer(required=True)
    # tags = fields.Nested(PlainTagSchema(), dump_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List( fields.Nested(PlainItemSchema()), dump_only = True)  # dump_only -> Only DB can dump(put) into this model, Not user #Load only - DB can load(take/bring it up) from the model
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class TagSchema(PlainTagSchema):
    items = fields.List( fields.Nested(PlainItemSchema()), dump_only = True  ) #TODO is it dump_only ? No, I guess
    store_id = fields.Integer( load_only = True ) 
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    

class ItemTagSchema(Schema):
    # id = fields.Int(dump_only=True)
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    pswd = fields.Str(required=True, load_only=True)  #since required is written here, can this schema be used for responding ??
