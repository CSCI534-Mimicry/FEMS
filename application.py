from flask import Flask, request, session
from flask import render_template, make_response
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
# import ml.mimic_face as mf
# import numpy as np
import random
import uuid
import base64
import os
from config import conn_str
import vh
import time

# EB looks for an 'application' callable by default.
application = Flask(__name__, static_folder="static/", static_url_path='')
application.config['SECRET_KEY'] = os.urandom(24)
give_list = [0, 1, 2, 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 10]
name_list = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James", "Isabella", "Oliver", "Sophia",
             "Benjamin", "Charlotte", "Elijah", "Mia"]
emotion_dict = {"neutral": "01", "calm": "02", "happy": "03", "sad": "04", "angry": "05", "fearful": "06",
                "disgust": "07", "surprised": "08"}
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = conn_str

db = SQLAlchemy(application)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(128), unique=True, nullable=False)
    user_step = db.Column(db.Integer)
    # Basic info
    sex = db.Column(db.String(32))
    age_group = db.Column(db.String(32))
    race_group = db.Column(db.String(128))
    # Section 2
    s2_a1_money = db.Column(db.Integer)
    s2_a1_similar = db.Column(db.Integer)
    s2_a1_human = db.Column(db.Integer)
    s2_a2_money = db.Column(db.Integer)
    s2_a2_similar = db.Column(db.Integer)
    s2_a2_human = db.Column(db.Integer)
    # Sequence
    s2_seq = db.Column(db.String(32))

    def __repr__(self):
        return '<Report %r>' % self.user_uuid


class Result_Section1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    opponent = db.Column(db.String(128))
    receive = db.Column(db.Integer)
    feel_file = db.Column(db.String(1024))
    feel_str = db.Column(db.String(16))
    send = db.Column(db.Integer)

    def __repr__(self):
        return '<Report %r>' % self.user_uuid

db.create_all()
db.session.commit()

def database_get_user(user_uuid):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    session["dir"] = str(user_uuid)
    session["sex"] = me.sex
    return me

def database_create_user(user_uuid):
    user_uuid = str(user_uuid)
    me = Result(user_uuid=user_uuid, user_step=0)
    db.session.add(me)
    db.session.commit()

def database_insert_bio_info(user_uuid, sex, age_group, race_group):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.sex = sex
    me.age_group = age_group
    me.race_group = race_group
    db.session.commit()

def database_insert_section1_play(user_uuid, opponent_name, round, money_receive, feel_file, feel_str, money_send):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    res = Result_Section1(user=me.id, round=round, opponent=opponent_name, receive=money_receive, feel_file=feel_file, feel_str=feel_str, send=money_send)
    db.session.add(res)
    db.session.commit()

def database_insert_money_to_agent1(user_uuid, money):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a1_money = money
    db.session.commit()

def database_insert_comment_to_agent1(user_uuid, similar, like_human):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a1_similar = similar
    me.s2_a1_human = like_human
    db.session.commit()

def database_insert_money_to_agent2(user_uuid, money):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a2_money = money
    db.session.commit()

def database_insert_comment_to_agent2(user_uuid, similar, like_human):
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a2_similar = similar
    me.s2_a2_human = like_human
    db.session.commit()

def database_update_user_sec2_seq(user_uuid, seqtype):
    # type: AB, BA
    user_uuid = str(user_uuid)
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_seq = seqtype
    db.session.commit()

@application.route("/index", methods=['GET'])
def index():
    session.clear()
    return application.send_static_file("index.html")


# require: index, give, name, submit_pic, dir
@application.route("/submit_emotion", methods=['POST'])
@cross_origin()
def submit_emotion():
    emotion = request.values.get("emotion")
    mny = request.values.get("mny")
    idx = session.get("index")
    share = session.get("give")
    pic_path = session.get("submit_pic", '')
    opponent = session.get("name")
    database_insert_section1_play(session.get("dir"), opponent, idx, share, pic_path, emotion, mny)

    return "success"


@application.route("/submit_question", methods=['POST'])
@cross_origin()
def submit_question():
    sex = request.values.get("sex")
    session["sex"] = sex
    age = request.values.get("age")
    race = request.values.get("race")
    session["dir"] = str(uuid.uuid4())
    os.mkdir("./static/img/testers/" + str(session["dir"]))
    os.mkdir("./static/img/testers/" + str(session["dir"]) + "/gnt")
    os.mkdir("./static/img/testers/" + str(session["dir"]) + "/ran")
    database_create_user(session.get("dir"))
    database_insert_bio_info(session.get("dir"), sex, age, race)
    res = make_response("success")
    return res


# require: idx2, dir
@application.route("/update_mny", methods=['POST'])
@cross_origin()
def update_mny():
    mny = request.values.get("mny")
    session["give"] = mny
    if session.get("idx2", 0) == 0:
        database_insert_money_to_agent1(session.get("dir"), mny)
    else:
        database_insert_money_to_agent2(session.get("dir"), mny)
    return "success"

# require: idx2, dir
def get_agent_pic_from_mny(mny, idx2 = -1):
    dir_name = session.get("dir")
    if idx2 == -1:
        idx2 = session.get("idx2")
    if idx2 == 1:
        if dir_name is None:
            result = "./img/actors/4/out-Rachel-0.png"
        else:
            result = "./img/testers/" + str(dir_name) + "/ran/" + str(mny) + ".png"
    else:
        if dir_name is None:
            result = "./img/actors/4/out-Rachel-0.png"
        else:
            result = "./img/testers/" + str(dir_name) + "/gnt/" + str(mny) + ".png"

    return result

@application.route("/submit_mny", methods=['POST'])
@cross_origin()
def submit_mny():
    mny = request.values.get("mny")
    session["give"] = mny
    return get_agent_pic_from_mny(mny)

@application.route("/current_usr", methods=['GET'])
def get_current_user():
    return str(session.get("dir"))

@application.route("/current_sec2_round", methods=['GET'])
def get_current_sec2_round():
    return str(session.get("idx2", 0))


# require: idx2, dir
@application.route("/submit_evaluation", methods=['POST'])
@cross_origin()
def submit_evaluation():
    similar, similar1 = request.values.get("similar"), request.values.get("similar1")
    treat, treat1 = request.values.get("treat"), request.values.get("treat1")
    me = database_get_user(session.get("dir"))
    if me.s2_seq == "AB":
        database_insert_comment_to_agent1(session.get("dir"), similar, treat)
        database_insert_comment_to_agent2(session.get("dir"), similar1, treat1)
    else:
        database_insert_comment_to_agent2(session.get("dir"), similar, treat)
        database_insert_comment_to_agent1(session.get("dir"), similar1, treat1)
    return "success"


# require: dir (user), give
@application.route("/submit_pic", methods=['POST'])
@cross_origin()
def submit_pic():
    rcv_data = request.values.get("img")
    dir_name = session.get("dir")
    print(dir_name)
    mny = session.get("give")
    file_path = './static/img/testers/' + str(dir_name) + '/' + str(mny) + '.jpg'
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(rcv_data))
    session["submit_pic"] = '/static/img/testers/' + str(dir_name) + '/' + str(mny) + '.jpg'
    return "success"


# require: index, dir
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
        name_ids_list = [i for i in range(14)]
        random.shuffle(name_ids_list)
        session["name_ids"] = name_ids_list
    else:
        idx = session.get("index") + 1
        session["index"] = idx

    name_id = session.get("name_ids")[idx]
    name = name_list[name_id]
    give = strategy_list[idx]
    receive = int(give) * 3
    img = "./img/agents/" + str(name_id + 1) + ".jpg"
    session["name"] = name
    session["give"] = give
    session["receive"] = receive

    context = {"name": name, "give": give, "receive": receive, "img": img}

    return render_template('phase1-0.html', **context)


# require: name, give, receive, dir
@application.route("/phase1-1", methods=['GET'])
def phase1_1():
    name = session.get("name")
    give = session.get("give")
    receive = session.get("receive")

    context = {"name": name, "give": give, "receive": receive}

    return render_template('phase1-1.html', **context)


# require: name, give, receive, dir
@application.route("/phase1-2", methods=['GET'])
def phase1_2():
    name = session.get("name")
    give = session.get("give")
    receive = session.get("receive")

    context = {"name": name, "give": give, "receive": receive}

    return render_template('phase1-2.html', **context)


# require: index, dir
@application.route("/phase1-3", methods=['GET'])
def phase1_3():
    idx = session.get("index")
    if idx == 13:
        return application.send_static_file("phase2-intro.html")
    else:
        return render_template('phase1-3.html')


# require: idx2, dir
@application.route("/phase2-1", methods=['GET'])
def phase2_1():
    if "user" in request.values:
        session.clear()
        database_get_user(request.values["user"])
    idx2 = session.get("idx2")
    if idx2 is None:
        session["idx2"] = (random.randint(1, 20000)) % 2
        session["idx2_time"] = 0
        if session.get("idx2") == 0:
            database_update_user_sec2_seq(session.get("dir"), "AB")
        else:
            database_update_user_sec2_seq(session.get("dir"), "BA")
    else:
        session["idx2"] = (idx2 + 1) % 2
        session["idx2_time"] = session.get("idx2_time") + 1

    img = get_agent_pic_from_mny(5)
    context = {"img": img}
    return render_template('phase2-1.html', **context)


# require: dir, give
@application.route("/phase2-2", methods=['GET'])
def phase2_2():
    give = session.get("give")
    if give is None:
        give = 5
    receive = int(give) * 3

    context = {"give": give, "receive": receive}
    return render_template('phase2-2.html', **context)


# require: dir
@application.route("/phase2-3", methods=['GET'])
def phase2_3():
    session["idx2_time"] = session.get("idx2_time", 1) + 1
    img0 = get_agent_pic_from_mny(5, (session.get("idx2") + 1) % 2)
    img1 = get_agent_pic_from_mny(5, session.get("idx2"))
    context = {"img0": img0, "img1": img1}
    return render_template('phase2-3.html', **context)


# require: dir
@application.route("/phase2-4", methods=['GET'])
def phase2_4():
    idx2 = session.get("idx2_time", -1)
    print(session.get("dir"), idx2)
    if idx2 == -1:
        return application.send_static_file("phase2-4-init.html")
    elif idx2 >= 2:
        session.clear()
        return application.send_static_file("final.html")
    elif idx2 >= 1:
        return application.send_static_file("phase2-5.html")
    else:
        return application.send_static_file("phase2-4.html")

# require: dir, give
@application.route("/generate-action-units-one-pic", methods=['GET'])
def generate_action_units_one_pic():
    share = session.get("give")
    pic_path = session.get("submit_pic", '')
    if pic_path != '':
        vh.purse_au_pic(share)
    return "Done"

# require: dir, sex
@application.route("/generate-action-units", methods=['GET'])
def generate_action_units():
    if "user" in request.values:
        database_get_user(str(request.values["user"]))
        vh.purse_au_pics(request.values["user"])
    else:
        vh.purse_au_pics()
    return "Done"

# require: dir
@application.route("/check-output-files", methods=['GET'])
def check_output_files():   
    usr_name = session.get("dir")
    out_files_dir = "./static/img/testers/" + str(usr_name) + "/gnt/"
    for i in range(11):
        while not os.path.exists(out_files_dir + str(i) + '.png'):
            time.sleep(1)
    out_files_dir = "./static/img/testers/" + str(usr_name) + "/ran/"
    for i in range(11):
        while not os.path.exists(out_files_dir + str(i) + '.png'):
            time.sleep(1)
    return "Done"

# require: dir
@application.route("/generate-compare-agent", methods=['GET'])
def generate_compare_agent():
    import shutil
    username = str(session.get("dir"))
    user_dir = "./static/img/testers/" + username + "/ran/"
    sex = session.get("sex", "")
    agent_dir = "./static/img/actors/6/"
    if sex == "male":
        agent_dir = "./static/img/actors/5/"
    file_list = os.listdir(agent_dir)
    random.shuffle(file_list)
    for i in range(len(file_list)):
        from_f = agent_dir + file_list[i]
        to_f = user_dir + str(i) + '.png'
        if os.path.exists(to_f):
            os.remove(to_f)
        shutil.copy(from_f, to_f)
    return "Done"

# require: dir
@application.route("/get-user-email", methods=['POST'])
@cross_origin()
def get_user_email():
    username = str(session.get("dir"))
    email = request.values.get("email")
    email_dir = "./static/img/testers/email"
    if not os.path.exists(email_dir):
        os.mkdir(email_dir)
    with open(email_dir + '/email-' + username + '.txt', 'w') as f:
        f.write(username + '\n' + email)
    return "Done"

def run():
    db.init_app(application)
    CORS(application, supports_credentials=True)
    # application.run(ssl_context='adhoc')
    application.run()

# run the app.
run()
