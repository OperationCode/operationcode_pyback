import json

from flask import Flask, request, make_response, redirect, url_for

from src.route_decorators import validate_response, url_verification
from src.routing_interface import combined_route_director
from utils.config import get_instance_folder_path
from utils import setup_logging
from utils.keys import VERIFICATION_TOKEN


app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='/static/templates')


@validate_response('token', VERIFICATION_TOKEN)
@app.route("/user_interaction", methods=['POST'])
def token_id_route():
    """
    Receives request from slack interactive messages.
    These are the messages that contain key: 'token_id'
    """
    data = json.loads(request.form['payload'])
    combined_route_director(data, 'callback')

    return make_response('', 200)


@app.route('/event_endpoint', methods=['POST'])
@url_verification
@validate_response('token', VERIFICATION_TOKEN)
def events_route():
    """
    Any event based response will get routed here.
    Decorates first make sure it's a verified route and this isn't a challenge event
    Lastly forwards event data to route director
    """
    response_data = request.get_json()
    combined_route_director(response_data, 'event')
    return make_response('', 200)


@app.route('/options_load', methods=['POST'])
def options_route():
    """
    Can provide dynamically created options for interactive messages.
    Currently unused.
    """
    return redirect(url_for('HTTP404'))


def start_server():
    setup_logging()
    app.run(debug=True)


if __name__ == '__main__':
    start_server()
