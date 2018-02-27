import datetime
import os
from functools import lru_cache

from flask import url_for, redirect, render_template

from ocbot import db
from ocbot.database.models_flask import TemporaryUrl, User
import logging

logger = logging.getLogger(__name__)


def get_temporary_url(user_id: str, text: str) -> TemporaryUrl:
    url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    if url and datetime.datetime.now() - url.created_on > datetime.timedelta(minutes=5):
        logger.info("URL expired before being used.  Making new one")
        db.session.delete(url)
        db.session.commit()
        url = None
    if not url:
        url = TemporaryUrl(slack_user=user_id)
        if text == 'debug':
            url.level = 'debug'
        else:
            url.level = 'info'
        db.session.add(url)
        db.session.commit()
        url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    return url


def handle_log_view(variable: str):
    url = TemporaryUrl.query.filter_by(url=variable).first()
    if not url:
        return redirect(url_for('HTTP403'))
    if datetime.datetime.now() - datetime.timedelta(minutes=5) > url.created_on:
        db.session.delete(url)
        logger.warning(f'Expired log requested from user id {url.slack_user}')
        return redirect(url_for('HTTP410'))  # Change this to a custom page

    db.session.delete(url)
    db.session.commit()

    f = open(f'logs/{url.level}.log')
    lines = list(f.readlines())
    lines = reversed(lines)
    older_logs = ''
    if os.path.isfile(f'logs/{url.level}.log.1'):
        f = open(f'logs/{url.level}.log.1')
        older_logs = list(f.readlines())
        older_logs = reversed(older_logs)
    return render_template("logs.html", logs=lines, older_logs=older_logs)


@lru_cache(100)
def can_view_logs(user_id: str):
    return bool(User.query.filter_by(slack_id=user_id, access_logs=True).first())
