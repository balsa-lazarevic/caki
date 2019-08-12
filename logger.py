import logging


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

# Create and configure logger
logging.basicConfig(filename="C:\\Users\\pc\\Desktop\\all_logs.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)

log = logging.getLogger()

