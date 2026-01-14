from app import db
from app.utils import distance, int_to_month
from datetime import timedelta

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
    is_cancelled = db.Column(db.Boolean, default=False, nullable=False)
    
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    end_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    driver = db.relationship('User', foreign_keys=[driver_id], back_populates='rides_driven')
    
    passengers = db.relationship('User', secondary=reservation_table, back_populates='booked_rides')

    start_location = db.relationship('Location', foreign_keys=[start_location_id])
    end_location = db.relationship('Location', foreign_keys=[end_location_id])

    reviews = db.relationship('Review', back_populates='ride')
    
    def get_month(self):
        return int_to_month(self.date.month)
    
    def get_day(self):
        return self.date.day
    
    def get_year(self):
        return self.date.year
    
    def get_departure_time(self):
        return self.date.strftime("%H:%M")
    
    def get_arrival_time(self):
        # Estimation simple basée sur une vitesse moyenne de 50 km/h
        dist = distance(self.start_location, self.end_location)
        hours = dist / 50.0
        arrival_time = self.date + timedelta(hours=hours)
        return arrival_time.strftime("%H:%M")