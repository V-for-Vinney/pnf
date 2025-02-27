import pyodbc
from peewee import Database

from .enums import Tables
from .models import *
from .serializers import ServerResponse


class AccessDatabase(Database):
    def __init__(self, database: str, password: str, driver: str, **kwargs):
        super().__init__(database, **kwargs)
        self.connection_string = "DRIVER={0};DBQ={1};PWD={2};ExtendedAnsiSQL=1;"
        self.driver = driver
        self.database = database
        self.password = password
        self.__conn = None

    def _connect(self):
        connection_string = self.connection_string.format(self.driver, self.database, self.password)
        conn = pyodbc.connect(connection_string)
        self.__conn = conn
        return conn

    def close(self):
        self.__conn.close()

    def cursor(self, commit=None, named_cursor=None):
        return self.__conn.cursor()


class DatabaseManager:
    def __init__(self, unit_generation: int, db_path: str, db_password: str):
        self._unit_generation = unit_generation
        self._db_path = db_path
        self._db_password = db_password
        if self._unit_generation == 1:
            self._driver = "{Microsoft Access Driver (*.mdb)};"
        else:
            self._driver = "{Microsoft Access Driver (*.mdb, *.accdb)};"
        self.conn = None
        self.allarmi = self._get_allarmi_model()
        self.suitcase = self._get_suitcase_model()
        self.settings = self._get_settings_model()

    def establish_connection(self):
        db_conn = AccessDatabase(database=self._db_path, password=self._db_password, driver=self._driver)
        db_conn.bind([self.allarmi, self.settings, self.suitcase])
        db_conn.connect()
        self.conn = db_conn

    def close_connection(self):
        self.conn.close()

    def is_local_data_consistent(self, table_name: str, server_response: ServerResponse):
        if table_name == Tables.suitcase.value:
            # в оригинальном коде nullable только поле "ID_Totale"
            if server_response.data.polycomm_id is None and server_response.data.partial_id is None:
                return True
            result = self.suitcase.select().where(
                (self.suitcase.id == server_response.data.polycomm_id) &
                (self.suitcase.id_totale == server_response.data.total_id) &
                (self.suitcase.id_parziale == server_response.data.partial_id)
            ).count()
        elif table_name == Tables.allarmi.value:
            result = self.allarmi.select().where(self.allarmi.id == server_response.data.polycomm_id).count()
        else:
            raise ValueError("Incorrect table name")
        return result != 0

    def get_data_delta(self, table_name: str, server_response: ServerResponse):
        if table_name == Tables.suitcase.value:
            query = self.suitcase.select().where(self.suitcase.id > server_response.data.polycomm_id)
        elif table_name == Tables.allarmi.value:
            query = self.allarmi.select().where(self.allarmi.id > server_response.data.polycomm_id)
        else:
            raise ValueError("Incorrect table name")
        return query

    def _get_allarmi_model(self):
        return {
            1: PolycommAllarmiModel,
            2: PackflyAllarmiModel,
            3: PackflyAllarmiModel,
        }.get(self._unit_generation)

    def _get_settings_model(self):
        return {
            1: PolycommSettingsModel,
            2: PackflySettingsModel,
            3: PackflySettingsModel,
        }.get(self._unit_generation)

    def _get_suitcase_model(self):
        return {
            1: PolycommSuitcaseModel,
            2: PackflySuitcaseModel,
            3: PackflySuitcaseModel,
        }.get(self._unit_generation)
