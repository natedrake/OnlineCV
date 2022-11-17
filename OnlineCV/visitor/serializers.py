# coding: utf-8
from marshmallow import (
    Schema, fields, pre_load, post_dump
)


class VisitorSchema(Schema):
    ip_address = fields.Str()
    user_agent = fields.Str()
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')
    # ugly hack.
    # user = fields.Nested('self', exclude=('user',), default=True, load_only=True)
    visitor = fields.Nested(lambda: VisitorSchema(exclude=('visitor',), default=True, load_only=True))

    @pre_load
    def make_visitor(self, data, **kwargs):
        data = data['visitor']
        # some of the frontends send this like an empty string and some send
        # null
        if not data.get('user_agent', True):
            del data['user_agent']
        if not data.get('created_at', True):
            del data['created_at']
        return data

    @post_dump
    def dump_visitor(self, data, **kwargs):
        return {'visitor': data}

    class Meta:
        strict = True

visitor_schema = VisitorSchema()
visitor_schemas = VisitorSchema(many=True)
