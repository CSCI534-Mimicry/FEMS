from flask import Flask, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
import json, uuid, os
import db

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_folder="static/")
application.config['SQLALCHEMY_DATABASE_URI'] = db.conn_str
db.db = SQLAlchemy(application)

@application.route("/index", methods=['GET'])
def index():
    uid = db.get_user_uuid()
    session['uid'] = uid
    print(uid)
    return application.send_static_file("index.html")


# run the app.
if __name__ == "__main__":
    application.secret_key = 'fake_KEY123'
    db.db.create_all()
    application.run()

