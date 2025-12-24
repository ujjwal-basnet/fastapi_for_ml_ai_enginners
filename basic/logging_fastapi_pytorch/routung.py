import logging 
from logging.handlers import RotatingFileHandler 

logger= logging.getLogger(name="rotating")
logger.setLevel(logging.INFO)

handler= RotatingFileHandler(filename="rotating_log.log", maxBytes=1000,backupCount=3)
logger.addHandler(handler)

for i in range(10000):
    logger.info(f"this is log line number {i}")