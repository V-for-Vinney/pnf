import sys
import time

import win32event
import win32service
import win32serviceutil

from app import CommunicationManager
from app import Config
from app import DatabaseManager
from app import ServiceState
from app import ServiceStatus
from app import Tables
from app import logger


# TODO: протестировать на WIn7, Win8.1, Win10, Win11

class MainProgram:
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
        if not response.data.status:
            logger.error("Отправка данных приостановлена сервером [{}]".format(table.value.upper()))
            # TODO: останавливать сервис?
        elif not self._db_mgr.is_local_data_consistent(table_name=table.value, server_response=response):
            self._comm_mgr.check_status_send(status=ServiceStatus.stopped_by_machine)
            logger.error("Отправка данных приостановлена клиентом [{}]".format(table.value.upper()))
            # TODO: останавливать сервис?
        else:
            self._db_mgr.establish_connection()
            data_delta = self._db_mgr.get_data_delta(table_name=table.value, server_response=response)
            rows_count = data_delta.count()
            self._db_mgr.close_connection()
            if rows_count == 0:
                logger.info("Нет новых записей [{}]".format(table.value.upper()))
            else:
                self._comm_mgr.send_table_data(table_type=table, table_data=data_delta)
                logger.info("Отправлено {} записей [{}]".format(len(data_delta), table.value.upper()))

    def sleep(self):
        time.sleep(self._config.sleep_timer_duration)


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PyPNFService"
    _svc_display_name_ = "PyPNFService"
    _svc_description_ = "Service sends locally stored Polycomm and Packfly data to remote server"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def SvcDoRun(self):
        self.running = True
        self._main()

    def _main(self):
        pnf = MainProgram("config.ini")
        pnf.send_state_online()
        pnf.get_db_password()
        if pnf.is_password_received():
            logger.info("Сервис стартовал")
            while self.running:
                try:
                    pnf.process_table(table=Tables.suitcase)
                    pnf.process_table(table=Tables.allarmi)
                    pnf.send_state_online()
                except KeyboardInterrupt:
                    sys.exit(0)
                except (ConnectionRefusedError, ConnectionError) as ex:
                    logger.error("Нет связи с сервером, пробую переподключиться... ({}).".format(ex))
                except Exception as ex:
                    logger.exception(ex)
                    break
                pnf.sleep()
        else:
            logger.error("Пароль к БД не получен")
        pnf.send_state_offline()
        logger.info("Сервис остановлен")


if __name__ == '__main__':
    try:
        win32serviceutil.HandleCommandLine(MyService)
    except Exception as ex:
        logger.exception(ex)
