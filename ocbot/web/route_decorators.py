import json
import logging
from functools import wraps

from flask import make_response, redirect, request

logger = logging.getLogger(__name__)


def validate_response(json_key, expected_value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                data = request.get_json()
                if not data:
                    data = request.data
            except Exception as e:
                return redirect('HTTP400.html', code=400)

            if json_key in data.keys() and data[json_key] != expected_value:
                return redirect('HTTP403.html', code=403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def url_verification(func):
    # @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
        except Exception as e:
            return redirect('HTTP400.html', code=400)

        if 'type' in data.keys() and data['type'] == 'url_verification':
            return make_response(json.dumps({'challenge': data['challenge']}), 200)

        return func(*args, **kwargs)

    return decorated_function
