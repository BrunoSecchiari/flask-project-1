from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), nullable=False, unique=False
    )
    items = db.relationship("ItemModel", back_populates="tags", secondary="item_tags")
    store = db.relationship("StoreModel", back_populates="tags")
