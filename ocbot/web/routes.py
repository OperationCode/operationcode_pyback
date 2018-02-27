from flask import request, make_response, redirect, url_for, render_template, json
import logging

from ocbot.web.slash_command_handlers import get_temporary_url, handle_log_view, can_view_logs
from ocbot.web.route_decorators import validate_response, url_verification
from ocbot.pipeline.routing import RoutingHandler
from config.configs import configs
from ocbot import app

VERIFICATION_TOKEN = configs['VERIFICATION_TOKEN']

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


@app.route("/get_logs", methods=['POST'])
def get_logs():
    """
    Endpoint used by Slack /logs command
    """
    req = request.values
    if req['token'] != VERIFICATION_TOKEN:
        return redirect(url_for('HTTP403'))
    logger.info(f'Log request received: {req}')

    if not can_view_logs(req['user_id']):
        logger.info(f"{req['user_name']} attempted to view logs and was denied")
        return make_response("You are not authorized to do that.", 200)

    url = get_temporary_url(req['user_id'])
    logger.info(f"Created log URL for {req['user_name']} : {url.url}")
    return make_response(f'{request.host_url}logs/{url.url}', 200)


@app.route("/logs/<variable>")
def show_logs(variable):
    return handle_log_view(variable)


@app.route("/zap_airtable_endpoint", methods=['POST'])
def zap_endpoint():
    """
    Endpoint for Zapier to send events when a new
    mentor request in submitted in airtable
    """
    data = request.get_json()
    logger.info(f'Zapier event received: {data}')
    RoutingHandler(data, route_id="new_airtable_request")
    return make_response('', 200)


@validate_response('token', VERIFICATION_TOKEN)
@app.route("/user_interaction", methods=['POST'])
def interaction_route():
    """
    Receives request from slack interactive messages.
    These are the messages that contain key: 'token_id'
    """
    data = json.loads(request.form['payload'])
    logger.info(f"Interaction received: {data}")
    route_id = data['callback_id']
    RoutingHandler(data, route_id=route_id)
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
    logger.debug(f'Event received: {json.dumps(response_data)}')
    route_id = response_data['event']['type']
    RoutingHandler(response_data, route_id=route_id)
    return make_response('', 200)


@app.route('/options_load', methods=['POST'])
def options_route():
    """
    Can provide dynamically created options for interactive messages.
    Currently unused.
    """
    return redirect(url_for('HTTP404'))


@app.route('/404')
def HTTP404():
    return render_template('HTTP404.html'), 404


@app.route('/403')
def HTTP403():
    return render_template('HTTP403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('HTTP404'))


@app.errorhandler(403)
def page_forbidden(error):
    return redirect(url_for('HTTP403'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
