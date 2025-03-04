import time
import warnings

from peewee import ModelSelect
from typing import Union

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import requests

from .enums import *
from .logger import logger
from .serializers import *
from .urls import Endpoints


class Schemas:
    def __init__(self, unit_generation: int):
        self.server_response = ServerResponseSchema()
        self.allarmi = self.get_allarmi_schema(unit_generation)
        self.suitcase = self.get_suitcase_schema(unit_generation)

    @staticmethod
    def get_allarmi_schema(unit_generation: int):
        return {
            1: AllarmiPolycommTableDataSchema(),
            2: AllarmiPackflyTableDataSchema(),
            3: AllarmiPackflyTableDataSchema(),
        }.get(unit_generation)

    @staticmethod
    def get_suitcase_schema(unit_generation: int):
        return {
            1: SuitcasePolycommTableDataSchema(),
            2: SuitcasePackflyTableDataSchema(),
            3: SuitcasePackflyTableDataSchema(),
        }.get(unit_generation)


class CommunicationManager:
    def __init__(
            self,
            server_url: str,
            machine_id: int,
            unit_generation: int,
            chunk_size: int = 1000,
            chunk_send_timeout: float = 0.1
    ):
        self.endpoints = Endpoints(server_url)
        self.schemas = Schemas(unit_generation)
        self.machine_id = machine_id
        self.unit_generation = unit_generation
        self.chunk_size = chunk_size
        self.chunk_send_timeout = chunk_send_timeout  # seconds
        self.logger = logger

    def send_state(self, state: ServiceState) -> bool:
        url = self.endpoints.service_state_request_url(self.machine_id, state=state)
        response = requests.get(url)
        return response.status_code == 200

    def check_status_send(self, status: ServiceStatus) -> bool:
        url = self.endpoints.check_status_request_url(self.machine_id, status)
        response = requests.get(url)
        json = response.json()
        server_response_data = self.schemas.server_response.load(json)
        return server_response_data.data["Data"]["Status"]

    def get_db_passwd(self) -> str:
        url = self.endpoints.db_request_url(self.machine_id)
        response = requests.get(url)
        json = response.json()
        server_response_data = self.schemas.server_response.load(json)
        return server_response_data.data["Data"]["DbPass"]

    def get_db_table_info(self, table: Tables) -> Union[ServerResponse, None]:
        url = self.endpoints.db_request_url(self.machine_id, table)
        response = requests.get(url)
        if not 200 <= response.status_code <= 299:
            self.logger.error("URL: {0}, ответ: {1} [{2}]".format(url, response.text, response.status_code))
            return
        json = response.json()
        server_response_dict = self.schemas.server_response.load(json).data
        server_response = ServerResponse(
            ResponseCode=server_response_dict["ResponseCode"],
            ResponseMessage=server_response_dict["ResponseMessage"],
            Data=ServerResponseData(**server_response_dict["Data"]),
        )
        return server_response

    def _chunkify(self, lst):
        for i in range(0, len(lst), self.chunk_size):
            yield lst[i:i + self.chunk_size]

    def send_table_data(self, table_type: Tables, table_data: ModelSelect):
        url = self.endpoints.base_url
        schema = self.schemas.allarmi if table_type == Tables.allarmi else self.schemas.suitcase
        for data_chunk in self._chunkify(table_data):
            payload_data = TableData(self.machine_id, table_type.value, list(data_chunk))
            payload_json = schema.dumps(payload_data)
            response = requests.post(url, json=payload_json.data)
            if not 200 <= response.status_code <= 299:
                chunk_ids = ",".join(str(entry.ID) for entry in data_chunk)
                msg = "Проблема при отправке данных '{0}' (ID: [{1}]). Ответ: {2}" \
                    .format(table_type.value.upper(), chunk_ids, response.text)
                self.logger.error(msg)
            time.sleep(self.chunk_send_timeout)
