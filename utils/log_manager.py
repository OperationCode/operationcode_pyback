import json
import logging.config
import os


# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def setup_logging(
        default_path='log_config.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
