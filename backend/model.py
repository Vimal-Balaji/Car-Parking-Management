from extensions import db
from init import app 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, primary_key=True,unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address=db.Column(db.String(200), nullable=True)

    def get_identity(self):
        return self.email
    
class OccupiedSlot(db.Model):
    __tablename__ = 'occupied_slot'
    slotId = db.Column(db.Integer, nullable=False, primary_key=True)
    lotId = db.Column(db.String(10), nullable=False, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['slotId', 'lotId'],
            ['slots.slotId', 'slots.lotId']
        ),
    )
    
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    vehicleNo = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)



class Locations(db.Model):
    __tablename__ = 'locations'
    location=db.Column(db.String(100), primary_key=True)
    address=db.Column(db.String(200), nullable=False)
    pincode=db.Column(db.String(6), nullable=False)

class Lots(db.Model):
    __tablename__ = 'lots'
    lotId = db.Column(db.String(10), primary_key=True)
    location= db.Column(db.String(100), db.ForeignKey('locations.location'), nullable=False)
    maxSlots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
class Slots(db.Model):
    __tablename__ = 'slots'
    slotId = db.Column(db.Integer,primary_key=True,nullable=False)
    lotId = db.Column(db.String(10), db.ForeignKey('lots.lotId'), nullable=False,primary_key=True)
    isOccupied = db.Column(db.Boolean, default=False, nullable=False)

def setup_database():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(userId=100000, name='admin', email='admin@example.com', password=generate_password_hash('admin123'))
            db.session.add(admin)
            db.session.commit()

