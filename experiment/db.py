# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# import random
# from sqlalchemy import ForeignKeyConstraint

# app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class User(db.Model):
#     __tablename__ = 'user'
#     userId = db.Column(db.Integer, primary_key=True,unique=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)

#     def get_identity(self):
#         return self.email
    
# class OccupiedSlot(db.Model):
#     __tablename__ = 'occupied_slot'
#     slotId = db.Column(db.Integer, nullable=False,primary_key=True)
#     lotId=db.Column(db.String(10), nullable=False,unique=True,primary_key=True)
#     userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False,unique=True)
#     startDate = db.Column(db.Date, nullable=False)
#     endDate = db.Column(db.Date, nullable=False)
#     startTime = db.Column(db.DateTime, nullable=False)
#     endTime = db.Column(db.DateTime, nullable=False)

    
#     __table_args__ = (
#         ForeignKeyConstraint(
#             ['slotId', 'lotId'],
#             ['slots.slotId', 'slots.lotId'],
#         ),
#     )


# class Locations(db.Model):
#     __tablename__ = 'locations'
#     location=db.Column(db.String(100), primary_key=True)
#     address=db.Column(db.String(200), nullable=False)
#     pincode=db.Column(db.String(6), nullable=False)

# class Lots(db.Model):
#     __tablename__ = 'lots'
#     lotId = db.Column(db.String(10), primary_key=True)
#     location= db.Column(db.String(100), db.ForeignKey('locations.location'), nullable=False)
#     maxSlots = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)
# class Slots(db.Model):
#     __tablename__ = 'slots'
#     slotId = db.Column(db.Integer,primary_key=True,nullable=False)
#     lotId = db.Column(db.String(10), db.ForeignKey('lots.lotId'), nullable=False,primary_key=True)
#     isOccupied = db.Column(db.Boolean, default=False, nullable=False)

# def gen_user_id():
#     while True:
#         rid = random.randint(100001, 999999)
#         if not User.query.filter_by(userId=rid).first():
#             return rid

# def gen_lot_id():
#     while True:
#         alpha1=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#         alpha2=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#         lotId= f"{alpha1}{alpha2}"
#         if not Locations.query.filter_by(lotId=lotId).first():
#             return lotId

# location = "salem"
# with app.app_context():
#     db.create_all()  # Ensure tables exist

#     location_entry = Locations.query.filter_by(location=location).first()
#     if location_entry:
#         lots = Lots.query.filter_by(location=location).all()

#         for lot in lots:
#             # First delete all occupied slots of this lot
#             occupied_slots = OccupiedSlot.query.filter_by(lotId=lot.lotId).all()
#             for occupied in occupied_slots:
#                 db.session.delete(occupied)

#             # Then delete all slots of this lot
#             slots = Slots.query.filter_by(lotId=lot.lotId).all()
#             for slot in slots:
#                 db.session.delete(slot)

#             # Finally delete the lot
#             db.session.delete(lot)

#         # Now delete the location itself
#         db.session.delete(location_entry)

#         db.session.commit()

import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Test connection
    r.ping()
    print("✅ Connected to Redis!")

    r.set("username", "vimal")
    username = r.get("username")
    print("Fetched from Redis:", username.decode())

except redis.exceptions.ConnectionError as e:
    print("❌ Could not connect to Redis. Make sure the server is running.")

