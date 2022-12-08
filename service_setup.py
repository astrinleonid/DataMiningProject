import logging
import json


with open("config.json", "r") as config_file:
    config = json.load(config_file)
# Create logger
logger = logging.getLogger('IMDB_parse')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
#

file_handler = logging.FileHandler(config["log_file"])
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)