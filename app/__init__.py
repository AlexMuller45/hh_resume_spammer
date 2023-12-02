import os
from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
app.config.from_object(os.environ.get("FLASK_ENV") or "config.DevelopmentConfig")


from . import views
from . import forms
from . import get_data
