from stream import app
from models import Event
Event.init_table()


app.run('0.0.0.0')
