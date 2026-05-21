from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel, StoreModel, TagModel
from schemas import ItemTagsSchema, TagSchema

blp = Blueprint("tags", __name__, description="Tag-Related Actions")


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class ItemTags(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def get(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message="An error ocurred while trying to insert the tag.")

        return tag

    @jwt_required()
    @blp.response(200, ItemTagsSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message="An error ocurred while trying to remove the tag.")

        return {"status": 200, "message": "The tag has been removed."}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(
        202,
        description="Delete a tag, if no item is related to it.",
        example={"message": "The tag has been deleted."},
    )
    @blp.alt_response(
        400,
        description="This occurs when a tag is related to one or more items, which would prevent the tag from being deleted.",
    )
    def delete(self, tag_id):
        jwt = get_jwt()

        if not jwt.get("is_admin"):
            abort(
                401,
                message="Administrator priviliges are required to perform this operation.",
            )

        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"status": 200, "message": "The tag has been deleted."}

        abort(400, message="An error ocurred while trying to delete the tag.")


@blp.route("/store/<int:store_id>/tag")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # if TagModel.query.filter(
        #     TagModel.name == tag_data["name"], TagModel.store_id == store_id
        # ).first():
        #     abort(400, message="A tag with that name already exists.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while trying to create the tag.")

        return tag
