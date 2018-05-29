import os
import logging

from flask import Config

logger = logging.getLogger(__name__)

configs = Config(os.path.dirname(__file__))
configs.from_object('config.default')

try:
    configs.from_envvar('CONFIG_FILE')
except RuntimeError as ex:
    logger.warning("Failed to load config from envar")
