from flask import Flask, request, session
from flask import render_template
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import ml.mimic_face as mf
import numpy as np
import random
import uuid
import base64
import os
import db as database
from config import conn_str

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_folder="static/")
application.config['SECRET_KEY'] = os.urandom(24)
give_list = [0, 0, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10]
name_list = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Oliver", "Sophia",
             "Benjamin", "Charlotte", "Elijah", "Mia"]
emotion_dict = {"neutral": "01", "calm": "02", "happy": "03", "sad": "04", "angry": "05", "fearful": "06",
                "disgust": "07", "surprised": "08"}
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = conn_str

db = SQLAlchemy(application)


@application.route("/index", methods=['GET'])
def index():
    return application.send_static_file("index.html")


@application.route("/submit_emotion", methods=['POST'])
@cross_origin()
def submit_emotion():
    emotion = request.values.get("emotion")
    mny = request.values.get("mny")
    idx = session.get("index")
    share = session.get("give")
    pic_path = session.get("submit_pic", '')
    opponent = session.get("name")
    database.insert_section1_play(session.get("dir"), opponent, idx, share, pic_path, emotion, mny)

    give = session.get("give")
    eid = emotion_dict[emotion]
    sex = session.get("sex")
    if sex == "male":
        hid = "1"
    else:
        hid = "2"
    file1 = "./static/img/actors/" + hid + "/" + eid + "-0.jpg"
    dir_name = session.get("dir")
    dir_name = "./static/img/testers/" + str(dir_name)

    file_list = os.listdir(dir_name)
    idx_list = list()
    if file_list is not None:
        for f_name in file_list:
            if f_name.split(".")[-1] == "jpg":
                idx = f_name.split(".")[0]
                idx_list.append(int(idx))
        id_list = np.array(idx_list)
        fid = np.argmin(np.abs(id_list - int(mny)))
        file2 = dir_name + file_list[int(fid)]
    else:
        file2 = "./static/img/actors/2/01-0.jpg"
    f, e = mf.handle_input(file1, file2)
    img = mf.handle_predict(f, e)
    mf.handle_output(img, dir_name + "/gnt/" + str(mny) + ".jpg")

    return "success"


@application.route("/submit_question", methods=['POST'])
@cross_origin()
def submit_question():
    sex = request.values.get("sex")
    session["sex"] = sex
    age = request.values.get("age")
    race = request.values.get("race")
    dir_name = session.get("dir")
    if dir_name is None:
        session["dir"] = uuid.uuid4()
        os.mkdir("./static/img/testers/" + str(session["dir"]))
        os.mkdir("./static/img/testers/" + str(session["dir"]) + "/gnt")
    database.create_user(session.get("dir"))
    database.insert_bio_info(session.get("dir"), sex, age, race)
    return "success"


@application.route("/update_mny", methods=['POST'])
@cross_origin()
def update_mny():
    mny = request.values.get("mny")
    session["give"] = mny
    if session.get("idx2", 0) == 0:
        database.insert_money_to_agent1(session.get("dir"), mny)
    else:
        database.insert_money_to_agent2(session.get("dir"), mny)
    return "success"


@application.route("/submit_mny", methods=['POST'])
@cross_origin()
def submit_mny():
    mny = request.values.get("mny")
    session["give"] = mny
    dir_name = session.get("dir")
    idx2 = session.get("idx2")
    if idx2 is not None and idx2 == 1:
        sex = session.get("sex")
        if sex == "male":
            return "./img/actors/1/01-0.jpg"
        else:
            return "./img/actors/2/01-0.jpg"
    if dir_name is None:
        result = "./img/actors/2/01-0.jpg"
    else:
        result = "./img/testers/" + str(dir_name) + "/gnt/" + str(mny) + ".jpg"

    return result


@application.route("/submit_evaluation", methods=['POST'])
@cross_origin()
def submit_evaluation():
    similar = request.values.get("similar")
    treat = request.values.get("treat")
    if session.get("idx2", 0) == 0:
        database.insert_comment_to_agent1(session.get("dir"), similar, treat)
    else:
        database.insert_comment_to_agent2(session.get("dir"), similar, treat)
    return "success"


@application.route("/submit_pic", methods=['POST'])
@cross_origin()
def submit_pic():
    rcv_data = request.values.get("img")
    dir_name = session.get("dir")
    mny = session.get("give")
    file_path = './static/img/testers/' + str(dir_name) + '/' + str(mny) + '.jpg'
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(rcv_data))
    session["submit_pic"] = '/static/img/testers/' + str(dir_name) + '/' + str(mny) + '.jpg'
    return "success"


@application.route("/phase1-0", methods=['GET'])
def phase1_0():
    session.permanent = True
    strategy_list = session.get("strategy")
    if strategy_list is None:
        strategy_list = give_list
        random.shuffle(strategy_list)
        session["strategy"] = strategy_list
        idx = 0
        session["index"] = idx
    else:
        idx = session.get("index") + 1
        session["index"] = idx

    name_id = random.randint(0, 13)
    name = name_list[name_id]
    give = strategy_list[idx]
    receive = int(give) * 3
    img = "./img/agents/" + str(name_id + 1) + ".jpg"
    session["name"] = name
    session["give"] = give
    session["receive"] = receive

    context = {"name": name, "give": give, "receive": receive, "img": img}

    return render_template('phase1-0.html', **context)


@application.route("/phase1-1", methods=['GET'])
def phase1_1():
    name = session.get("name")
    give = session.get("give")
    receive = session.get("receive")

    context = {"name": name, "give": give, "receive": receive}

    return render_template('phase1-1.html', **context)


@application.route("/phase1-2", methods=['GET'])
def phase1_2():
    name = session.get("name")
    give = session.get("give")
    receive = session.get("receive")

    context = {"name": name, "give": give, "receive": receive}

    return render_template('phase1-2.html', **context)


@application.route("/phase1-3", methods=['GET'])
def phase1_3():
    idx = session.get("index")
    if idx == 13:
        return application.send_static_file("phase2-intro.html")
    else:
        return render_template('phase1-3.html')


@application.route("/phase2-1", methods=['GET'])
def phase2_1():
    idx2 = session.get("idx2")
    if idx2 is None:
        session["idx2"] = 0
    else:
        session["idx2"] = idx2 + 1

    img = "./img/agents/1.jpg"
    context = {"img": img}
    return render_template('phase2-1.html', **context)


@application.route("/phase2-2", methods=['GET'])
def phase2_2():
    give = session.get("give")
    if give is None:
        give = 5
    receive = int(give) * 3

    context = {"give": give, "receive": receive}
    return render_template('phase2-2.html', **context)


@application.route("/phase2-3", methods=['GET'])
def phase2_3():
    img = "./img/agents/1.jpg"
    context = {"img": img}
    return render_template('phase2-3.html', **context)


@application.route("/phase2-4", methods=['GET'])
def phase2_4():
    idx2 = session.get("idx2")
    if idx2 is not None and idx2 == 1:
        return application.send_static_file("final.html")
    else:
        return application.send_static_file("phase2-4.html")

def run():
    db.init_app(application)
    CORS(application, supports_credentials=True)
    application.run(debug=True, ssl_context='adhoc')

# run the app.
if __name__ == "__main__":
    run()
