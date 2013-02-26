import json

import psycopg2
from psycopg2.extras import DictCursor

import config


class Event(object):

    conn = psycopg2.connect(
        database=config.PG_DB,
        user=config.PG_USER,
        password=config.PG_PASS,
        host=config.PG_HOST,
        port=config.PG_PORT
    )

    @classmethod
    def _cursor(self):
        return self.conn.cursor(cursor_factory=DictCursor)

    @staticmethod
    def _prep_data(events):
        times = set()
        for e in events:
            e['info'] = json.loads(e['info'])
            times.add(e['time'])

        if len(times) > 0:
            last = max(times)
        else:
            last = None

        return (events, last)

    @classmethod
    def init_table(self):
        cur = self._cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events
            (
                id serial PRIMARY KEY UNIQUE,
                service text,
                info text,
                time timestamp,
                event_id text UNIQUE
            );
            """
        )
        self.conn.commit()
        cur.close()

    @classmethod
    def new(self, service, info, e_time, e_id):
        status = {
            'success': True,
            'error': None
        }
        e_id = '{0}_{1}'.format(service, e_id)
        if isinstance(info, dict):
            info = json.dumps(info)
        elif isinstance(info, str):
            # Check if info is valid json
            json.loads(info)

        cur = self._cursor()
        try:
            cur.execute(
                """
                INSERT INTO events
                (service, info, time, event_id)
                VALUES (%s, %s, %s, %s)
                """, (service, info, e_time, e_id)
            )
            self.conn.commit()
        except psycopg2.IntegrityError:
            status['success'] = False
            status['error'] = 'Event already exists'
            self.conn.rollback()
        finally:
            cur.close()

        return status

    @classmethod
    def latest(self, limit=config.EVENT_AMOUNT):
        cur = self._cursor()
        cur.execute(
            'SELECT * FROM events ORDER BY time DESC LIMIT %s',
            (limit,)
        )

        events = cur.fetchall()
        return self._prep_data(events)

    @classmethod
    def since(self, time):
        cur = self._cursor()
        cur.execute(
            """
            SELECT * FROM events WHERE time > %s
            ORDER BY time DESC
            """, (time,)
        )

        events = cur.fetchall()
        return self._prep_data(events)
