from app import db

from datetime import datetime
from flask_login import UserMixin

from app.models.ride import ride_passengers

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    upjv_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15))
    
    # Informations véhicule (seulement si conducteur)
    vehicle_model = db.Column(db.String(100))
    vehicle_color = db.Column(db.String(50))
    license_plate = db.Column(db.String(20))
    max_seats = db.Column(db.Integer)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    rides_taken = db.relationship('Ride', secondary=ride_passengers,
                                   back_populates='passengers', lazy='dynamic')
    rides_given = db.relationship('Ride', back_populates='driver', 
                                   cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} ({self.upjv_id})>'