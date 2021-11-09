import logging
import time

from custom_handler import CustomBufferingHandler

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger()
logger.addHandler(CustomBufferingHandler(capacity=5, time=5, max_buffer_size=100))


if __name__ == '__main__':

    for i in range(7):
        logger.info("Hello log World")
        time.sleep(1)

    logging.shutdown()
