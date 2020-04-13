from flask import Flask, request, session
import json
import uuid

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_folder="static/")


@application.route("/index", methods=['GET'])
def index():
    session['uid'] = uuid.uuid4()
    print(session['uid'])
    return application.send_static_file("index.html")


# run the app.
if __name__ == "__main__":
    application.secret_key = 'fake_KEY123'
    application.run()

