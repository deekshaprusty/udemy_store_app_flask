from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from models import StoreModel, TagModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("Tags", "tags", description = "Operation on tags")

@blp.route('/store/<string:store_id>/tag')
class Tag(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(id=store_id)
        return store.tags.all()
        

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500, message = str(ex) )
        return tag