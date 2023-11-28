import os
from flask import Flask


app = Flask(__name__)
app.config.from_object(os.environ.get("FLASK_ENV") or "config.DevelopmentConfig")


from . import views
