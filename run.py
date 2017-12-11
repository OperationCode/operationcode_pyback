import logging

from src.app import run_bot
from utils.log_manager import setup_logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    setup_logging()
    run_bot()
