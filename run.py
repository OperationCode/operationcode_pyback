import os

if 'CONFIG_FILE' not in os.environ:
    os.environ['CONFIG_FILE'] = 'development.py'

if __name__ == '__main__':
    from ocbot.web.app import start_server
    start_server()
