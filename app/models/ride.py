from app import db

# Table d'association pour la relation many-to-many entre Ride et User (passagers)
reservation_table = db.Table('reservation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('ride_id', db.Integer, db.ForeignKey('ride.id'), primary_key=True)
)

class Ride(db.Model):
    __tablename__ = 'ride'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    end_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    driver = db.relationship('User', foreign_keys=[driver_id], back_populates='rides_driven')
    
    passengers = db.relationship('User', secondary=reservation_table, back_populates='booked_rides')

    start_location = db.relationship('Location', foreign_keys=[start_location_id])
    end_location = db.relationship('Location', foreign_keys=[end_location_id])

    reviews = db.relationship('Review', back_populates='ride')