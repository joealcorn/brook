import sys
from datetime import datetime
sys.path.append('..')

from flask import (
    render_template,
    make_response,
    redirect,
    jsonify,
    request,
    url_for,
)

from stream import app
from models import Event as Events


@app.route('/')
def index():
    (events, last) = Events.latest()
    response = make_response(
        render_template('stream.html', events=events)
    )
    response.set_cookie('last_event',  last)
    return response


@app.route('/update')
def update():
    last_event = request.cookies.get('last_event')
    if last_event is None:
        return redirect(url_for('index'))

    last_event = datetime.strptime(last_event, '%Y-%m-%d %H:%M:%S')

    (events, last) = Events.since(last_event)

    info = {
        'events': []
    }

    info['amount'] = len(info['events'])
    for event in events:
        info['events'].append({
            'service': event['service'],
            'html': render_template(
                'services/{0}.html'.format(event['service']),
                e=event
            )
        })

    response = make_response(jsonify(info))
    response.headers['Cache-Control'] = 'no-cache'

    if events == [] or last is None:
        return response
    else:
        response.set_cookie('last_event',  last)
        return response
