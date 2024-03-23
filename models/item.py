from db import db
import sys


class ItemModel(db.Model):
    __tablename__ = "items"
    print(f'Debugging : ItemModel ')
    sys.stdout.flush()
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    price = db.Column(db.Float(precision=2), unique=False, nullable = False )
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique = False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items", )
    # tag_ids = db.Column(db.List)
    # tags = db.relationship("Tags") #code for M to M