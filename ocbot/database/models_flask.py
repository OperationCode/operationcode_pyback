from uuid import uuid4

from ocbot import db


class TemporaryUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slack_user = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String, default=lambda: uuid4().hex, unique=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Temp URL for {self.slack_user}: {self.url} created at {self.created_on}"
