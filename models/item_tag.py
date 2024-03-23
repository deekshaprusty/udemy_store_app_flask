# # from flask_sqlalchemy import SQLAlchemy
# from db import db

# class ItemTag(db.Model):
#     __tablename__ = "ItemTag"
#     id = db.Column(db.Integer, primary_key = True)
#     itemId = db.Column(db.Integer, db.ForeignKey("items.id"), unique=False)
#     tagId = db.Column(db.Integer, db.ForeignKey("tags.id"), unique=False)