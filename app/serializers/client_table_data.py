from marshmallow import Schema, fields

from .client_row_data_allarmi import AllarmiPackflyRowDataSchema
from .client_row_data_allarmi import AllarmiPolycommRowDataSchema
from .client_row_data_suitcase import SuitcasePackflyRowDataRowDataSchema
from .client_row_data_suitcase import SuitcasePolycommRowDataRowDataSchema


class _BaseTableDataSchema(Schema):
    machineId = fields.Integer(required=True)
    dataType = fields.String(required=True)


class AllarmiPolycommTableDataSchema(_BaseTableDataSchema):
    records = fields.List(fields.Nested(AllarmiPolycommRowDataSchema), required=True)


class AllarmiPackflyTableDataSchema(_BaseTableDataSchema):
    records = fields.List(fields.Nested(AllarmiPackflyRowDataSchema), required=True)


class SuitcasePolycommTableDataSchema(_BaseTableDataSchema):
    records = fields.List(fields.Nested(SuitcasePolycommRowDataRowDataSchema), required=True)


class SuitcasePackflyTableDataSchema(_BaseTableDataSchema):
    records = fields.List(fields.Nested(SuitcasePackflyRowDataRowDataSchema), required=True)


class TableData:
    def __init__(self, machine_id: int, data_type: str, records: list):
        self.machineId = machine_id
        self.dataType = data_type
        self.records = records
