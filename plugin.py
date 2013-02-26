from brook.models import Event

loaded = []


class Plugin(object):
    """
    Base plugin class

    """

    def __init__(self, name):
        loaded.append((name, self))
        self.name = name

    def main(self):
        """
        This is the entry point for all plugins.
        Plugins should gather the appropriate data
        and then call self.insert_data

        """
        pass

    def insert_data(self, event_id, time, info):
        """
        Inserts data into a database

        time: should be a datetime object, preferably UTC
        info: dict or json that will be used in templates

        """
        status = Event.new(self.name, info, time, event_id)
        return status
