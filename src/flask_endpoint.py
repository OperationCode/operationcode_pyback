import json

from flask import Flask, request, make_response

from keys import VERIFICATION_TOKEN
from src import app as bot
from utils.log_manager import setup_logging
# from pprint import pprint

app = Flask(__name__)


@app.route("/user_interaction", methods=['POST'])
def interaction():
    """
    Receives requests from Slack's interactive messages
    """

    data = json.loads(request.form['payload'])
    if data['token'] != VERIFICATION_TOKEN:
        # TODO Logger here
        print("Bad request")
        return make_response("", 403)

    callback = data['callback_id']
    # pprint(data['user'])

    if callback == 'greeting_buttons':
        bot.help_menu_interaction(data)
    elif callback == 'greeted':
        bot.greeted_interaction(data)
    elif callback == 'suggestion_modal':
        # pprint(data)
        bot.suggestion_submission(data)
    elif callback == 'mentor_request':
        # pprint(data)
        bot.mentor_submission(data)
    return make_response('', 200)


@app.route('/options_load', methods=['POST'])
def options_load():
    """
    Can provide dynamically created options for interactive messages.
    Currently unused.
    """
    return make_response('', 404)


@app.route('/event_endpoint', methods=['POST'])
def challenge():
    """
    Endpoint for all subscribed events
    """
    payload = {}
    data = request.get_json()

    # pprint(data)

    if data['token'] != VERIFICATION_TOKEN:
        print("Bad request")
        return make_response("", 403)
    if data['type'] == 'url_verification':
        payload['challenge'] = data['challenge']
        return make_response(json.dumps(payload), 200)
    else:
        bot.event_handler(data['event'])
        return make_response('', 200)


def start_server():
    setup_logging()
    app.run(debug=True)


if __name__ == '__main__':
    start_server()
