import logging

print(dir(logging))

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

# Create and configure logger
logging.basicConfig(filename="C:\\Users\\pc\\Desktop\\all_logs.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)

log = logging.getLogger()

# Test the logger
log.debug("This is harmless debug message.")
log.info("Just some useful info.") # level for info log -> 20 (20 < 30 and wont be saved to file, because we need to set level)
log.warning("This is some warning, you should fix it.")
log.error("Did you just tried to divide by zero? This can crush your program.")
log.critical("Server is down.")


print(log.level)
