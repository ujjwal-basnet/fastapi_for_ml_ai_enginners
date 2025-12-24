import logging 

logger= logging.getLogger("non_rotating")
logger.setLevel(logging.INFO)

handler= logging.FileHandler("non_rotating.log")
logger.addHandler(handler)

for i in range(100000):
    logger.info(f"this si the line number {i}")
    
