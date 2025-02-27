from urllib.parse import *

from .enums import *


class Endpoints:
    def __init__(self, base_url: str):
        # если не поставить "/" в конце urljoin отработает некорректно
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.db = urljoin(self.base_url, "db")
        self.state = urljoin(self.base_url, "state")
        self.check = urljoin(self.base_url, "check")

    @staticmethod
    def _build_url(endpoint: str, query_params: dict) -> str:
        return str(urlunparse(urlparse(endpoint)._replace(query=urlencode(query_params))))

    def db_request_url(self, machine_id, tb_name: Tables = None) -> str:
        query_params = {
            "id": machine_id,
        }
        if tb_name:
            query_params["tb_name"] = tb_name.value
        return self._build_url(self.db, query_params)

    def check_status_request_url(self, machine_id, status: ServiceStatus) -> str:
        query_params = {
            "id": machine_id,
            "status": status.value,
        }
        return self._build_url(self.db, query_params)

    def service_state_request_url(self, machine_id, state: ServiceState) -> str:
        query_params = {
            "id": machine_id,
            "stateval": state.value,
        }
        return self._build_url(self.state, query_params)
