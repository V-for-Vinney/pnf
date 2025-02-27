from marshmallow import Schema, fields


class _BaseAllarmiRowDataSchema(Schema):
    id = fields.Integer(required=True, load_from='ID', dump_to='ID')
    data = fields.DateTime(required=True, load_from='Data', dump_to='Data')
    messagio = fields.String(required=True, load_from='Messaggio', dump_to='Messaggio')


class AllarmiPolycommRowDataSchema(_BaseAllarmiRowDataSchema):
    new = fields.Bool(required=True, load_from='New', dump_to='New')
    total_suitcase = fields.Integer(required=True, load_from='Total_Suitcase', dump_to='Total_Suitcase')


class AllarmiPackflyRowDataSchema(_BaseAllarmiRowDataSchema):
    pass
