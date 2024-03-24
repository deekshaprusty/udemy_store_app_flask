from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from models import StoreModel, TagModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
import sys

blp = Blueprint("Tags", "tags", description = "Operation on tags")

@blp.route('/stores/<string:store_id>/tag')
class Tag(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        print(f'tag GET store_id : {store_id}, type(store_id) : {type(store_id)}')
        sys.stdout.flush()        
        store = StoreModel.query.get_or_404(store_id)
        # tags = TagModel.query.all()
        return store.tags.all()
        # return tags
        

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        print(f'tag POST store_id : {store_id}, type(store_id) : {type(store_id)}')
        sys.stdout.flush()
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500, message = str(ex) )
        return tag