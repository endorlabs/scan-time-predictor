import logging
def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler('log/log.txt'),
            logging.StreamHandler()
        ]
    )

# Call the configure_logging function when this module is imported
configure_logging()

def getLogger ():
    # Create a logger
    logger = logging.getLogger('logger')
    return logger