from extensions import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    email = fields.Email(required=True)
    adresse = fields.String()


class FavoriteSchema(ma.Schema):
    destination_id = fields.Int(required=True)