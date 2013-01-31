import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from brook import config

loaded = []
engine = create_engine(config.DATABASE, echo=False)
Base = declarative_base()
session = sessionmaker(bind=engine)
Session = session()


class Brook(Base):
    __tablename__ = 'brook'

    id = Column(Integer, primary_key=True)
    service = Column(String(64), nullable=False)
    info = Column(String(9999), nullable=False)
    time = Column(DateTime, nullable=False)
    event_id = Column(String(128), nullable=False, unique=True)

    def __init__(self, service, info, time, event_id):
        self.service = service
        self.info = info
        self.time = time
        self.event_id = event_id


# Create table if it doesn't already exist
Base.metadata.create_all(engine)


class Plugin(object):
    """
    Base plugin class

    """

    database = config.DATABASE
    init = None

    def __init__(self, name):
        loaded.append((name, self))
        self.name = name

    def main(self):
        """
        This is the entry point for all plugins

        """
        pass

    def _id_exists(self, event_id):
        """
        Checks if `event_id` is already in the database

        """
        event_id = '{0}_{1}'.format(self.name, event_id)

        query = Session.query(Brook).filter_by(event_id=event_id).distinct()
        items = [i for i in query]

        if items == []:
            return False
        else:
            return True

    def insert_data(self, event_id, time, info):
        """
        Inserts data into a database

        time: should be a datetime object, preferably UTC
        info: dict or json that will be used in templates

        """

        if isinstance(info, dict):
            info = json.dumps(info)
            pass
        elif isinstance(info, str):
            # Check if info is valid json
            json.loads(info)

        if not self._id_exists(event_id):
            event_id = '{0}_{1}'.format(self.name, event_id)
            items = Brook(self.name, info, time, event_id)
            Session.add(items)
            Session.commit()
