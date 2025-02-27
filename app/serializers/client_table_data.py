from marshmallow import Schema, fields

from .client_row_data_allarmi import AllarmiPackflyRowDataSchema
from .client_row_data_allarmi import AllarmiPolycommRowDataSchema
from .client_row_data_suitcase import SuitcasePackflyRowDataRowDataSchema
from .client_row_data_suitcase import SuitcasePolycommRowDataRowDataSchema


class _BaseTableDataSchema(Schema):
    machine_id = fields.Integer(required=True, load_from='machine_id', dump_to='machineId')
    data_type = fields.String(required=True, load_from='data_type', dump_to='dataType')


class AllarmiPolycommTableDataSchema(_BaseTableDataSchema):
    records = fields.List(
        fields.Nested(AllarmiPolycommRowDataSchema),
        required=True,
        load_from='records',
        dump_to='records'
    )


class AllarmiPackflyTableDataSchema(_BaseTableDataSchema):
    records = fields.List(
        fields.Nested(AllarmiPackflyRowDataSchema),
        required=True,
        load_from='records',
        dump_to='records'
    )


class SuitcasePolycommTableDataSchema(_BaseTableDataSchema):
    records = fields.List(fields.Nested(
        SuitcasePolycommRowDataRowDataSchema),
        required=True,
        load_from='records',
        dump_to='records'
    )


class SuitcasePackflyTableDataSchema(_BaseTableDataSchema):
    records = fields.List(
        fields.Nested(SuitcasePackflyRowDataRowDataSchema),
        required=True,
        load_from='records',
        dump_to='records'
    )


class TableData:
    def __init__(self, machine_id: int, data_type: str, records: list):
        self.machine_id = machine_id
        self.data_type = data_type
        self.records = records
