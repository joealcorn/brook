import sys
import json
sys.path.append('..')

from flask import render_template

from stream import app, Brook


@app.route('/')
def index():
    events = Brook.query.order_by(Brook.time.desc()).limit(30).all()
    for event in events:
        event.info = json.loads(event.info)

    return render_template('stream.html', events=events)
