from db import db




class UserModel(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique =True)
    pswd = db.Column(db.String)