import datetime
from functools import lru_cache

from flask import url_for, redirect, render_template

from ocbot import db
from ocbot.database.models_flask import TemporaryUrl, User
import logging

logger = logging.getLogger(__name__)


def get_temporary_url(user_id):
    url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    if url and datetime.datetime.now() - url.created_on > datetime.timedelta(minutes=5):
        logger.info("URL expired before being used.  Making new one")
        db.session.delete(url)
        db.session.commit()
        url = None
    if not url:
        url = TemporaryUrl(slack_user=user_id)
        db.session.add(url)
        db.session.commit()
        url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    return url


def handle_log_view(variable):
    url = TemporaryUrl.query.filter_by(url=variable).first()
    if not url:
        return redirect(url_for('HTTP403'))
    if datetime.datetime.now() - datetime.timedelta(minutes=5) > url.created_on:
        db.session.delete(url)
        logger.warning(f'Expired log requested from user id {url.slack_user}')
        return redirect(url_for("HTTP403"))  # Change this to a custom page
    db.session.delete(url)
    db.session.commit()

    f = open('logs/debug.log')
    lines = list(f.readlines())
    lines = reversed(lines)
    return render_template("logs.html", logs=lines)

@lru_cache(50)
def can_view_logs(user_id: str):
    return bool(User.query.filter_by(slack_id=user_id).first())
