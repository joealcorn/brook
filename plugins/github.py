from datetime import datetime

import requests

from brook import plugin, config


date_format = '%Y-%m-%dT%H:%M:%SZ'


class GitHub(plugin.Plugin):

    def main(self):
        url = 'https://api.github.com/users/{0}/events'
        r = requests.get(url.format(config.GITHUB_USER))

        if 'message' in r.json:
            print 'GitHub: ' + r.json['message']
            return

        for event in r.json:
            # Execute function of the same name as the Event Type
            # Hacky way of doing it, would like to find a nicer way
            if event['type'] in globals():
                # Each event should return a dict with every value
                # it needs to build the HTML templates

                event_info = globals()[event['type']](event)

                if not self._id_exists(event_info[0]):
                    self.insert_data(*event_info)
                else:
                    # We're only going to find events
                    # we've already got in the DB
                    return


def event_handler(func):
    """
    This decorator takes the event_id and event_time
    from the json so events only need to return `info`

    """

    def wrapper(event):
        info = func(event)
        if 'type' not in info:
            info.update({'type': event['type']})

        event_id = event['id']
        event_time = datetime.strptime(event['created_at'], date_format)
        return (event_id, event_time, info)

    return wrapper


@event_handler
def PushEvent(event):
    info = {
        'repo': event['repo']['name'],
        'amount': event['payload']['size'],
        'commits': event['payload']['commits']
    }

    return info


@event_handler
def WatchEvent(event):
    info = {
        'repo': event['repo']['name'],
        'action': event['payload']['action']
    }

    return info


@event_handler
def FollowEvent(event):
    info = {
        'user': event['payload']['target']['login']
    }

    return info


@event_handler
def IssuesEvent(event):
    info = {
        'action': event['payload']['action'],
        'repo': event['repo']['name'],
        'number': event['payload']['issue']['number'],
        'title': event['payload']['issue']['title']

    }

    return info

# Register our plugin
GitHub('GitHub')
