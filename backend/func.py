from model import User,Lots
import random

def gen_user_id():
    while True:
        rid = random.randint(100001, 999999)
        if not User.query.filter_by(userId=rid).first():
            return rid

def gen_lot_id():
    while True:
        alpha1=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        alpha2=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        lotId= f"{alpha1}{alpha2}"
        if not Lots.query.filter_by(lotId=lotId).first():
            return lotId