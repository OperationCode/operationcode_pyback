import json
import logging
from functools import wraps

from flask import make_response, redirect, url_for, request

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')


def validate_response(json_key, expected_value):
    def decorator(funct):
        @wraps(funct)
        def wrapper(*args, **kwargs):
            data = json.loads(request.form['payload'])[json_key]
            if data is not expected_value:
                return redirect(url_for('HTTP403'))

            return funct(data, *args, **kwargs)

        return wrapper

    return decorator


def url_verification(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        if data['type'] is 'url_verification':
            return make_response(json.dumps({'challenge': data['challenge']}), 200)

        return f(*args, **kwargs)

    return decorated_function
