import sys
import json
from datetime import datetime
sys.path.append('..')

from flask import render_template, jsonify, make_response, request, url_for, redirect

from stream import app, Brook as b


@app.route('/')
def index():
    times = []
    events = b.query.order_by(b.time.desc()).limit(app.config['EVENT_AMOUNT']).all()

    for event in events:
        event.info = json.loads(event.info)
        times.append(event.time)

    response = make_response(render_template('stream.html', events=events))
    response.set_cookie('last_event',  max(times))
    return response


@app.route('/update')
def update():
    last_event = request.cookies.get('last_event')
    if last_event is None:
        return redirect(url_for('index'))

    last_event = datetime.strptime(last_event, '%Y-%m-%d %H:%M:%S')

    events = b.query.order_by(b.time.desc()).filter(b.time > last_event).limit(
        app.config['EVENT_AMOUNT']).all()

    times = []
    info = {'events': []}

    for event in events:
        times.append(event.time)
        event.info = json.loads(event.info)
        info['events'].append({
            'service': event.service,
            'html': render_template('services/{0}.html'.format(event.service), e=event)
        })

    info['amount'] = len(info['events'])

    response = make_response(jsonify(info))
    response.headers['Cache-Control'] = 'no-cache'

    if events == []:
        return response
    else:
        response.set_cookie('last_event',  max(times))
        return response
