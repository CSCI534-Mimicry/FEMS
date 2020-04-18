import uuid
from application import dbAlchemy as db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(128), unique=True, nullable=False)
    user_step = db.Column(db.Integer)
    # Basic info
    sex = db.Column(db.String(32))
    age_group = db.Column(db.String(32))
    race_group = db.Column(db.String(128))
    # Section 1
    # s1_opponent = db.Column(db.String(128))
    # s1_user_role = db.Column(db.Integer)
    # s1_results = db.relationship('Result_Section1', backref='result', lazy=True)
    # Section 2
    s2_a1_money = db.Column(db.Integer)
    s2_a1_similar = db.Column(db.Integer)
    s2_a1_human = db.Column(db.Integer)
    s2_a2_money = db.Column(db.Integer)
    s2_a2_similar = db.Column(db.Integer)
    s2_a2_human = db.Column(db.Integer)

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

def get_user_uuid():
    res = uuid.uuid4()
    return res

def create_user(user_uuid):
    me = Result(user_uuid=user_uuid, user_step=0)
    db.session.add(me)
    db.session.commit()

def insert_bio_info(user_uuid, sex, age_group, race_group):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.sex = sex
    me.age_group = age_group
    me.race_group = race_group
    db.session.commit()

def insert_section1_play(user_uuid, opponent_name, round, money_receive, feel_file, feel_str, money_send):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    res = Result_Section1(user=me.id, round=round, opponent=opponent_name, receive=money_receive, feel_file=feel_file, feel_str=feel_str, send=money_send)
    db.session.add(res)
    db.session.commit()

def insert_money_to_agent1(user_uuid, money):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a1_money = money
    db.session.commit()

def insert_comment_to_agent1(user_uuid, similar, like_human):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a1_similar = similar
    me.s2_a1_human = like_human
    db.session.commit()

def insert_money_to_agent2(user_uuid, money):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a2_money = money
    db.session.commit()

def insert_comment_to_agent2(user_uuid, similar, like_human):
    me = Result.query.filter_by(user_uuid=user_uuid).first()
    me.s2_a2_similar = similar
    me.s2_a2_human = like_human
    db.session.commit()