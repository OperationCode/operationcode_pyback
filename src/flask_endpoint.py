from flask import Flask, request, Response
from decouple import config
import json
from src import app as bot
from pprint import pprint

from utils.log_manager import setup_logging

app = Flask(__name__)

VERIFICATION_TOKEN = config('APP_VERIFICATION_TOKEN')


@app.route('/', methods=['POST'])
def challenge():
    pprint(request.get_json())
    payload = {}
    data = request.get_json()
    if data['token'] != VERIFICATION_TOKEN:
        print("Bad request")
        return ''
    if data['type'] == 'url_verification':
        payload['challenge'] = data['challenge']
    else:
        bot.event_handler(data['event'])
    print(payload)
    return json.dumps(payload)


if __name__ == '__main__':
    setup_logging()
    app.run(debug=True)
