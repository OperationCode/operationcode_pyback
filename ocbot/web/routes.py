from flask import request, make_response, redirect, url_for, render_template, json, jsonify, send_file, \
    after_this_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import logging
import threading
import os

from werkzeug.datastructures import FileStorage

from ocbot.pipeline.slash_command_handlers.log_handlers import get_temporary_url, handle_log_view, can_view_logs
from ocbot.pipeline.web_api_handlers.handle_code_school import handle_recaptcha_and_errors
from ocbot.pipeline.slash_command_handlers.lunch_handler import create_lunch_event
from ocbot.pipeline.slash_command_handlers.testgreet_handler import can_test, create_testgreet_event
from ocbot.web.route_decorators import validate_response, url_verification
from ocbot.pipeline.routing import RoutingHandler
from config.configs import configs
from ocbot import app

VERIFICATION_TOKEN = configs['VERIFICATION_TOKEN']

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr in ["127.0.0.1", "localhost"]


@app.route('/event_endpoint', methods=['POST'])
@url_verification
@validate_response('token', VERIFICATION_TOKEN, 'json')
def events_route():
    """
    Any event based response will get routed here.
    Decorates first make sure it's a verified route and this isn't a challenge event
    Lastly forwards event data to route director
    """
    response_data = request.get_json()
    logger.debug(f'Event received: {json.dumps(response_data)}')
    route_id = response_data['event']['type']
    threading.Thread(target=RoutingHandler,
                     kwargs={"json_data": response_data, 'route_id': route_id}).start()
    # RoutingHandler(response_data, route_id=route_id)
    return make_response('', 200)


@app.route("/user_interaction", methods=['POST'])
@validate_response('token', VERIFICATION_TOKEN, 'form')
def interaction_route():
    """
    Receives request from slack interactive messages.
    These are the messages that contain key: 'token_id'
    """
    data = json.loads(request.form['payload'])
    logger.info(f"Interaction received: {data}")
    route_id = data['callback_id']
    threading.Thread(target=RoutingHandler,
                     kwargs={'json_data': data, 'route_id': route_id}).start()
    # RoutingHandler(data, route_id=route_id)
    return make_response('', 200)


@app.route("/zap_airtable_endpoint", methods=['POST'])
def zap_endpoint():
    """
    Endpoint for Zapier to send events when a new
    mentor request in submitted in airtable
    """
    data = request.get_json()
    logger.info(f'Zapier event received: {data}')
    threading.Thread(target=RoutingHandler,
                     kwargs={'json_data': data, 'route_id': 'new_airtable_request'}).start()
    # RoutingHandler(data, route_id="new_airtable_request")
    return make_response('', 200)


@app.route("/new_code_school")
def new_code_school():
    data = request.get_json()


@app.route('/test/testgreet', methods=['POST'])
@validate_response('token', VERIFICATION_TOKEN, 'values')
def test_greet():
    """
    Endpoint for simulating a Slack 'team_join' event.
    Sends the notification to whichever channel the user
    was in when running the slash-command
    """
    req = request.values
    logger.info(f"testgreet received from {req['user_name']} : {req}")
    if not can_test(req['user_id']):
        logger.info(f"{req['user_name']} attempted to testgreet and was denied")
        return make_response("You are not authorized to do that.", 200)

    event = create_testgreet_event(req)
    threading.Thread(target=RoutingHandler,
                     kwargs={'json_data': event, 'route_id': 'team_join'}).start()
    # RoutingHandler(event, route_id='team_join')
    return make_response('Test completed.', 200)


@app.route("/get_logs", methods=['POST'])
@validate_response('token', VERIFICATION_TOKEN, 'values')
def get_logs():
    """
    Endpoint used by Slack /logs command
    """
    req = request.values
    logger.info(f'Log request received: {req}')

    if not can_view_logs(req['user_id']):
        logger.info(f"{req['user_name']} attempted to view logs and was denied")
        return make_response("You are not authorized to do that.", 200)

    url = get_temporary_url(req['user_id'], req['text'])
    logger.info(f"Created log URL for {req['user_name']} : {url.url}")
    return make_response(f'{request.host_url}logs/{url.url}', 200)


@app.route('/lunch', methods=['POST'])
@validate_response('token', VERIFICATION_TOKEN, 'values')
def random_lunch():
    """
    Endpoint for getting random lunch event.
    Sends the notification to whichever channel the user
    was in when running the slash-command
    """
    req = request.values
    logger.info(f"Lunch request received from {req['user_name']} : {req}")

    lunch_val = create_lunch_event(req)

    return make_response(lunch_val, 200)


@app.route("/logs/<variable>")
def show_logs(variable):
    return handle_log_view(variable)


@app.route("/add_code_school", methods=['POST'])
@limiter.limit("5/hour;1/minute")
def add_new_school():
    '''
    This route recieves the post from the /new_school form
    :return:
    '''
    imagefile: FileStorage

    try:
        imagefile = request.files['school_logo']
        if imagefile:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename)
            imagefile.save(filename)

    except Exception as e:
        print(e)

    if not imagefile:
        return ''

    return handle_recaptcha_and_errors(request, imagefile)


@app.route('/images/<filename>')
def get_image(filename):
    filepath = os.path.join('web', 'imageStore', filename)
    file_handle = open(os.path.join('ocbot', filepath), 'r')

    @after_this_request
    def remove_file(response):
        try:
            os.remove(os.path.join('ocbot', filepath))
            file_handle.close()

        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filepath)


@app.route("/new_school", methods=['GET'])
def code_school_form():
    """
    This is the route to render the new codeschool form.
    :return:
    """
    return render_template("code_school.html")


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


@app.route('/410')
def HTTP410():
    return render_template('HTTP410.html'), 410


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('HTTP404'))


@app.errorhandler(403)
def page_forbidden(error):
    return redirect(url_for('HTTP403'))


@app.errorhandler(410)
def page_gone(error):
    return redirect(url_for('HTTP410'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
