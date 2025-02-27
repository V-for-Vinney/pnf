import configparser
import os


class Config:
    def __init__(self, config_file_path: str):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("No config file '{}'".format(config_file_path))
        parser = configparser.ConfigParser()
        try:
            parser.read(config_file_path, encoding='utf-8')
        except configparser.MissingSectionHeaderError:
            parser.read(config_file_path, encoding='utf-8-sig')
        except UnicodeDecodeError:
            parser.read(config_file_path, encoding='cp1251')
        self.machine_id = int(parser['PNF']['MACHINE_ID'])
        self.db_path = parser['PNF']['DB_PATH']
        self.unit_generation = int(parser['PNF']['UNIT_GENERATION'])
        self.dashboard_url = parser['PNF']['DASHBOARD_URL']
        self.data_chunk_size = int(parser['PNF']['DATA_CHUNK_SIZE'])
        self.sleep_timer_duration = float(parser['PNF']['TIMER_DURATION'])
        self.chunk_send_timeout = float(parser['PNF']['CHUNK_SEND_TIMEOUT'])
        self.db_passwd = None
