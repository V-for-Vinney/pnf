import logging
import os
from logging.handlers import TimedRotatingFileHandler

logs_path = "./logs/"
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler(
    logs_path + "pnf_service.log",
    when='midnight',
    backupCount=90,
    encoding='utf-8',
)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
