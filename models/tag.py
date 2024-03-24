from db import db


class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique = True, nullable=False) #Tutor did nullable=False. Lets see without that
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="tags")
    
    items = db.relationship("ItemModel", back_populates="tags", secondary = "items_tags" )  #write code for M to M 


# class ItemsTagsModel(db.Model):
#     __tablename__ = 'items_tags'
#     id = db.Column(db.Integer, primary_key = True)
#     item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
#     tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))