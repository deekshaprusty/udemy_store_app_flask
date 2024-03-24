from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, ItemSchema
from models import StoreModel, TagModel, ItemsTagsModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
import sys

blp = Blueprint("Tags", "tags", description = "Operation on tags")
# blp_item_tag = Blueprint()

@blp.route('/stores/<string:store_id>/tags')
class TagsInStore(MethodView):

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



#Link and Unlink tags and items
@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkItemsTags(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except Exception as ex:
            abort(500, message=f"Error occurred while inserting tag: {str(ex)}")
        return tag

    @blp.response(200, TagSchema) # This is different from what Instructor did. Try out whats different.
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except Exception as ex:
            abort(500, message=f'error occurred while deleting tag from item : {str(ex)}')

        return {"message": "Tag removed from item", 'tag' : tag, 'item' : item}



@blp.route('/tags/<string:tag_id>')
class Tags(MethodView):  #Rename the class and fix everything

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    # @blp.response(200, TagSchema)
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "tag deleted" } #, "tag" : tag}
        abort(400, message="Could not delete tag. Make sure tag is not associated with any item")




@blp.route('/items/<string:item_id>/tags')
class TagsInItems(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item.tags


@blp.route('/tags/<string:tag_id>/items')
class ItemsInTags(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag.items