import logging
import os

import pytest

logger = logging.getLogger(__name__)

from config.all_config_loader import configs


def test_using_development_config():
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    # from config.all_config_loader import configs


@pytest.mark.parametrize("test_input", [item for item in configs.keys()])
def test_configs_not_default(test_input):
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    from config.all_config_loader import configs
    assert (configs[test_input] != 'default')


@pytest.mark.parametrize("test_input", [item for item in configs.keys()])
def test_configs_not_empty(test_input):
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    from config.all_config_loader import configs
    assert (configs[test_input] != '')
