from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE']

db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)


class Brook(db.Model):
    __tablename__ = 'brook'

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(64), nullable=False)
    info = db.Column(db.String(9999), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    event_id = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, service, info, time, event_id):
        self.service = service
        self.info = info
        self.time = time
        self.event_id = event_id


import stream.views
import stream.filters
