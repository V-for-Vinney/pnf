from marshmallow import Schema, fields
from typing import Union


class _DataSuitResponseSchema(Schema):
    polycomm_id = fields.Int(load_from='Polycommid', dump_to='Polycommid', allow_none=True)
    total_id = fields.Int(required=True, load_from='Totalid', dump_to='Totalid', allow_none=True)
    partial_id = fields.Int(required=True, load_from='Partialid', dump_to='Partialid', allow_none=True)
    total = fields.Int(required=True, load_from='Total', dump_to='Total', allow_none=True)
    status = fields.Bool(required=True, load_from='Status', dump_to='Status', allow_none=True)
    db_pass = fields.Str(required=True, load_from='DbPass', dump_to='DbPass', allow_none=True)


class ServerResponseSchema(Schema):
    response_code = fields.Int(required=True, load_from='ResponseCode', dump_to='ResponseCode', allow_none=True)
    response_msg = fields.Str(required=True, load_from='ResponseMessage', dump_to='ResponseMessage', allow_none=True)
    data = fields.Nested(_DataSuitResponseSchema, required=True, load_from='Data', dump_to='Data')


class ServerResponseData:
    def __init__(
            self,
            polycomm_id: int,
            status: bool,
            db_pass: str,
            total_id: Union[int, None] = None,
            partial_id: Union[int, None] = None,
            total: Union[int, None] = None,
    ):
        self.polycomm_id = polycomm_id
        self.total_id = total_id
        self.partial_id = partial_id
        self.total = total
        self.status = status
        self.db_pass = db_pass


class ServerResponse:
    def __init__(self, response_code: int, response_msg: str, data: ServerResponseData):
        self.response_code = response_code
        self.response_msg = response_msg
        self.data = data
        self._patch_null_data_fields()

    def _patch_null_data_fields(self):
        if self.data.polycomm_id is None:
            self.data.polycomm_id = 0
        if self.data.total_id is None:
            self.data.total_id = 0
        if self.data.partial_id is None:
            self.data.partial_id = 0
