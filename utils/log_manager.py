import json
import logging.config
import os
import decouple

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')


# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def setup_logging(default_level=logging.INFO):

    logging_config = decouple.config('LOGGING_CONFIG', default='log_config.json')
    file_path = os.path.join(os.path.dirname(__file__), logging_config)

    if os.path.exists(file_path):
        with open(file_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)
        logger.warning('Warning, verify there is no desired config file')
