from app import db

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    licence_plate = db.Column(db.String(20), unique=True, nullable=False)
    max_seats = db.Column(db.Integer, nullable=False)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    owner = db.relationship('User', back_populates='vehicle')