from ..core import db


class ResourceMixin():
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
