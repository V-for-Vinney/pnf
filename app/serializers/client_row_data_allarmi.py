from marshmallow import Schema, fields


class _BaseAllarmiRowDataSchema(Schema):
    ID = fields.Integer(required=True)
    Data = fields.DateTime(required=True)
    Messaggio = fields.String(required=True)


class AllarmiPolycommRowDataSchema(_BaseAllarmiRowDataSchema):
    New = fields.Bool(required=True)
    Total_Suitcase = fields.Integer(required=True)


class AllarmiPackflyRowDataSchema(_BaseAllarmiRowDataSchema):
    pass
