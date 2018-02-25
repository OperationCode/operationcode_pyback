import os

if 'CONFIG_FILE' not in os.environ:
    os.environ['CONFIG_FILE'] = 'development.py'

if __name__ == '__main__':
    from ocbot import app
    app.run(port=5000, debug=True)
