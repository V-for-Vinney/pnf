from marshmallow import Schema, fields


class _BaseSuitcaseRowDataSchema(Schema):
    id = fields.Integer(required=True, load_from='ID', dump_to='ID')
    id_totale = fields.Integer(required=True, load_from='ID_Totale', dump_to='ID_Totale')
    id_parziale = fields.Integer(required=True, load_from='ID_Parziale', dump_to='ID_Parziale')
    data_ini = fields.DateTime(required=True, load_from='Data_ini', dump_to='Data_ini')
    esito = fields.Bool(required=True, load_from='Esito', dump_to='Esito')
    barcode = fields.String(required=True, load_from='Barcode', dump_to='Barcode')
    id_user_name = fields.Integer(required=True, load_from='ID_UserName', dump_to='ID_UserName')
    data_fine = fields.DateTime(required=True, load_from='Data_Fine', dump_to='Data_Fine')


class SuitcasePolycommRowDataRowDataSchema(_BaseSuitcaseRowDataSchema):
    barcode = fields.Integer(required=True, load_from='Barcode', dump_to='Barcode')
    id_user_name = fields.Integer(required=True, load_from='ID_Utente', dump_to='ID_Utente')
    data_fine = fields.DateTime(required=True, load_from='Data', dump_to='Data')
    ko_peso = fields.Bool(required=True, load_from='KO_Peso', dump_to='KO_Peso')
    ko_stop = fields.Bool(required=True, load_from='KO_STOP', dump_to='KO_STOP')
    allarme_on = fields.Bool(required=True, load_from='Allarme_ON', dump_to='Allarme_ON')
    id_macchina = fields.Integer(required=True, load_from='ID_Macchina', dump_to='ID_Macchina')


class SuitcasePackflyRowDataRowDataSchema(_BaseSuitcaseRowDataSchema):
    ricetta = fields.Integer(required=True, load_from='Ricetta', dump_to='Ricetta')
    allarme = fields.Integer(required=True, load_from='Allarme', dump_to='Allarme')
