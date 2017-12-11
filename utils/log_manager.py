import json
import logging.config
import os

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')


# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def setup_logging(default_path='log_config.json',
                  default_level=logging.INFO
                  ):
    file_path = os.path.join(os.path.dirname(__file__), default_path)

    if os.path.exists(file_path):
        with open(file_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)
        logger.warning('Warning, verify there is no desired config file')
