from functools import wraps

from sqlalchemy.exc import IntegrityError


def validate_integrity(func):
    """
    Decorator that wraps any function that interacts with the database and could cause
    an IntegrityError, catching the exception and returning the desired result
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError:
            return False
    return inner