from marshmallow import Schema, fields


class _BaseSuitcaseRowDataSchema(Schema):
    ID = fields.Integer(required=True)
    ID_Totale = fields.Integer(required=True)
    ID_Parziale = fields.Integer(required=True)
    Data_ini = fields.DateTime(required=True)
    Esito = fields.Bool(required=True)
    Barcode = fields.String(required=True)
    ID_UserName = fields.Integer(required=True)
    Data_Fine = fields.DateTime(required=True)


class SuitcasePolycommRowDataRowDataSchema(_BaseSuitcaseRowDataSchema):
    Barcode = fields.Integer(required=True)
    ID_Utente = fields.Integer(required=True)
    Data = fields.DateTime(required=True)
    KO_Peso = fields.Bool(required=True)
    KO_STOP = fields.Bool(required=True)
    Allarme_ON = fields.Bool(required=True)
    ID_Macchina = fields.Integer(required=True)


class SuitcasePackflyRowDataRowDataSchema(_BaseSuitcaseRowDataSchema):
    Ricetta = fields.Integer(required=True)
    Allarme = fields.Integer(required=True)
