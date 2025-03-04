import time

from .communication_manager import CommunicationManager
from .config_parser import Config
from .database_manager import DatabaseManager
from .enums import ServiceState
from .enums import ServiceStatus
from .enums import Tables
from .logger import logger
from .exceptions import DataTransferStoppedByMachineError
from .exceptions import DataTransferStoppedByServerError


class DataProcessor:
    def __init__(self, config_path: str):
        self._config = Config(config_path)
        self._comm_mgr = CommunicationManager(
            server_url=self._config.dashboard_url,
            chunk_size=self._config.data_chunk_size,
            unit_generation=self._config.unit_generation,
            machine_id=self._config.machine_id,
            chunk_send_timeout=self._config.chunk_send_timeout,
        )
        self._db_mgr = None
        self.logger = logger

    def send_state_online(self):
        self._comm_mgr.send_state(ServiceState.online)

    def send_state_offline(self):
        self._comm_mgr.send_state(ServiceState.offline)

    def get_db_password(self):
        self._config.db_passwd = self._comm_mgr.get_db_passwd()
        self._db_mgr = DatabaseManager(
            unit_generation=self._config.unit_generation,
            db_path=self._config.db_path,
            db_password=self._config.db_passwd,
        )

    def is_password_received(self) -> bool:
        return bool(self._config.db_passwd)

    def process_table(self, table: Tables):
        response = self._comm_mgr.get_db_table_info(table=table)
        if not response:
            return
        if not response.Data.Status:
            msg = "Отправка данных приостановлена сервером [{}]".format(table.value.upper())
            self.logger.error(msg)
            raise DataTransferStoppedByServerError(msg)
        elif not self._db_mgr.is_local_data_consistent(table_name=table.value, server_response=response):
            self._comm_mgr.check_status_send(status=ServiceStatus.stopped_by_machine)
            msg = "Отправка данных приостановлена клиентом [{}]".format(table.value.upper())
            self.logger.error(msg)
            raise DataTransferStoppedByMachineError(msg)
        else:
            self._db_mgr.establish_connection()
            data_delta = self._db_mgr.get_data_delta(table_name=table.value, server_response=response)
            if data_delta.count() != 0:
                self._comm_mgr.send_table_data(table_type=table, table_data=data_delta)
                self.logger.info("Отправлено {} записей [{}]".format(len(data_delta), table.value.upper()))
            self._db_mgr.close_connection()

    def sleep(self):
        time.sleep(self._config.sleep_timer_duration)
