import os


def pytest_sessionstart(session):
    """ before session.main() is called. """
    os.environ['CONFIG_FILE'] = 'tests.py'
    os.environ['test-oc'] = ''
