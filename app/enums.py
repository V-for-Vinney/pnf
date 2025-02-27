__all__ = [
    "Tables",
    "ServiceState",
    "ServiceStatus",
]

from enum import Enum


class ServiceState(Enum):
    online = 1
    offline = 2
    passwd_ok = 3
    passwd_fail = 4
    passwd_not_received = 5


class ServiceStatus(Enum):
    stopped_by_machine = 0
    stopped_by_server = 1


class Tables(Enum):
    allarmi = "Allarmi"
    suitcase = "Suitcase"
