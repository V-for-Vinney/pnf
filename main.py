import sys
import threading

import win32event
import win32service
import win32serviceutil

from app import DataProcessor
from app import DataTransferStoppedByMachineError
from app import DataTransferStoppedByServerError
from app import Tables
from app import logger

CONFIG_PATH = "config.ini"
IS_RUNNING_GLOBAL_FLAG = True


# TODO: протестировать на WIn7, Win8.1, Win10, Win11.
# TODO: осталась проблема с открытым соединением с БД, пока не будут отправлены все чанки.
# TODO: писать лог не в файл, а в системный журнал.

class PyPNFService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PyPNFService"
    _svc_display_name_ = "PyPNFService"
    _svc_description_ = "Service sends locally stored Polycomm and Packfly data to remote server"

    def __init__(self, args):
        logger.debug("Svc__init__")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.service_thread = None
        self.data_processor = DataProcessor(CONFIG_PATH)

    def SvcDoRun(self):
        """Основной метод запуска сервиса."""
        logger.debug("SvcDoRun")
        try:
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            global IS_RUNNING_GLOBAL_FLAG
            IS_RUNNING_GLOBAL_FLAG = True
            self.service_thread = threading.Thread(target=self.run)
            self.service_thread.start()
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        except Exception as ex:
            logger.exception(ex)
            self.SvcStop()

    def SvcStop(self):
        """Остановка сервиса."""
        logger.debug("SvcStop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        global IS_RUNNING_GLOBAL_FLAG
        IS_RUNNING_GLOBAL_FLAG = False
        if self.service_thread:
            self.service_thread.join()
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    @staticmethod
    def run():
        """Основная логика сервиса в отдельном потоке."""
        pnf = DataProcessor("config.ini")
        logger.info("Сервис стартовал")
        pnf.send_state_online()
        pnf.get_db_password()
        logger.info("Пароль к БД получен")
        if pnf.is_password_received():
            global IS_RUNNING_GLOBAL_FLAG
            while IS_RUNNING_GLOBAL_FLAG:
                logger.debug("Итерация цикла...")
                try:
                    pnf.process_table(table=Tables.suitcase)
                    pnf.process_table(table=Tables.allarmi)
                    pnf.send_state_online()
                except (DataTransferStoppedByServerError, DataTransferStoppedByMachineError):
                    pass
                except KeyboardInterrupt:
                    IS_RUNNING_GLOBAL_FLAG = False
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
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        PyPNFService.run()
    else:
        win32serviceutil.HandleCommandLine(PyPNFService)
