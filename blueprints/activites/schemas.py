from extensions import ma
from marshmallow import fields, validate

class ActivitySchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf(["transport", "loisir", "repas"])
    )
    price_estimated = fields.Float(required=True)
    destination_id = fields.Int(required=True)

class EcoPlanRequestSchema(ma.Schema):
        activities = fields.List(
            fields.Nested(ActivitySchema),
            required=True,
            validate=validate.Length(min=1),
            error_messages={"required": "La liste d'activités est obligatoire"}
        )