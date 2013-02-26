from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_pyfile('../config.py')

toolbar = DebugToolbarExtension(app)

import stream.views
import stream.filters
