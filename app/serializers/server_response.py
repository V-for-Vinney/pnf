from marshmallow import Schema, fields
from typing import Union


class _DataSuitResponseSchema(Schema):
    Polycommid = fields.Int(allow_none=True)
    Totalid = fields.Int(required=True, allow_none=True)
    Partialid = fields.Int(required=True, allow_none=True)
    Total = fields.Int(required=True, allow_none=True)
    Status = fields.Bool(required=True, allow_none=True)
    DbPass = fields.Str(required=True, allow_none=True)


class ServerResponseSchema(Schema):
    ResponseCode = fields.Int(required=True, allow_none=True)
    ResponseMessage = fields.Str(required=True, allow_none=True)
    Data = fields.Nested(_DataSuitResponseSchema, required=True)


class ServerResponseData:
    def __init__(
            self,
            Polycommid: int,
            Status: bool,
            DbPass: str,
            Totalid: Union[int, None] = None,
            Partialid: Union[int, None] = None,
            Total: Union[int, None] = None,
    ):
        self.Polycommid = Polycommid
        self.Totalid = Totalid
        self.Partialid = Partialid
        self.Total = Total
        self.Status = Status
        self.DbPass = DbPass


class ServerResponse:
    def __init__(self, ResponseCode: int, ResponseMessage: str, Data: ServerResponseData):
        self.ResponseCode = ResponseCode
        self.ResponseMessage = ResponseMessage
        self.Data = Data
        self._patch_null_data_fields()

    def _patch_null_data_fields(self):
        if self.Data.Polycommid is None:
            self.Data.Polycommid = 0
        if self.Data.Totalid is None:
            self.Data.Totalid = 0
        if self.Data.Partialid is None:
            self.Data.Partialid = 0
