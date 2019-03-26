import os
import config
from flask import Flask
from models.base_model import db

api_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'my_api')

app = Flask('my-assessment', root_path=api_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@app.route("/", methods=["GET"])
def index():

    return "HOMEPAGE - Backend"