from app import db
from datetime import datetime

ride_passengers = db.Table('ride_passengers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('ride_id', db.Integer, db.ForeignKey('ride.id', ondelete='CASCADE'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class Ride(db.Model):
    __tablename__ = 'ride'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Localisation
    from_location = db.Column(db.String(200), nullable=False)
    to_location = db.Column(db.String(200), nullable=False)
    from_lat = db.Column(db.Float, nullable=False)
    from_lng = db.Column(db.Float, nullable=False)
    to_lat = db.Column(db.Float, nullable=False)
    to_lng = db.Column(db.Float, nullable=False)
    
    # Horaire
    departure_time = db.Column(db.DateTime, nullable=False, index=True)
    estimated_arrival = db.Column(db.DateTime) 
    
    # Places
    available_seats = db.Column(db.Integer, nullable=False)
    
    # Informations supplémentaires
    notes = db.Column(db.Text) 
    status = db.Column(db.String(20), default='active') # active, completed, cancelled
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), 
                          nullable=False, index=True)
    driver = db.relationship('User', back_populates='rides_given')
    passengers = db.relationship('User', secondary=ride_passengers, 
                                 back_populates='rides_taken', lazy='dynamic')
    
    @property
    def is_full(self):
        return self.passengers.count() >= self.available_seats
    
    @property
    def remaining_seats(self):
        return self.available_seats - self.passengers.count()

    def __repr__(self):
        return f'<Ride {self.id}>'
