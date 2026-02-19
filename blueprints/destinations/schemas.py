from extensions import ma
from marshmallow import fields

class DestinationSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    city = fields.String(required=True)
    country = fields.String(required=True)
    description = fields.String()