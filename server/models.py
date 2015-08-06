from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    battery_percent = db.Column(db.Integer)
    status = db.Column(db.Text)

    def __init__(self, username, battery_percent, status):
        self.username = username
        self.battery_percent = battery_percent
        self.status = status

    def __repr__(self):
        return '<Data for %r>' % self.username