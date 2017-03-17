from flask import Flask

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Import a module / component using its blueprint handler variable
from app.taiga_gitlab.controllers import taiga_gitlab

# Register blueprint(s)
app.register_blueprint(taiga_gitlab)
