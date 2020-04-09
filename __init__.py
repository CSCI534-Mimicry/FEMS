from flask import Flask, request
import json

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_folder="static/")


@application.route("/index", methods=['GET'])
def index():
    return application.send_static_file("index.html")


# run the app.
if __name__ == "__main__":
    application.run()

