from uuid import uuid4

from ocbot import db


class TemporaryUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slack_user = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String, default=lambda: uuid4().hex, unique=True)
    level = db.Column(db.String(32), default="info")
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Temp URL for {self.slack_user}: {self.url} created at {self.created_on}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slack_id = db.Column(db.String(32), index=True, unique=True)
    slack_name = db.Column(db.String(32), index=True)
    access_logs = db.Column(db.Boolean, default=False)
    can_test = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<User id:{self.id} | slack_id: {self.slack_id} | slack_name: {self.slack_name} | access_logs: {self.access_logs}>'
