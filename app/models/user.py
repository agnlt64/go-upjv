from app import db
from datetime import datetime
from app.models.ride import reservation_table
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    upjv_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    vehicle = db.relationship('Vehicle', back_populates='owner', uselist=False)
    
    # Un utilisateur conduit plusieurs trajets
    rides_driven = db.relationship('Ride', back_populates='driver', foreign_keys='Ride.driver_id')

    # Un utilisateur peut être passager de plusieurs trajets
    booked_rides = db.relationship('Ride', secondary=reservation_table, back_populates='passengers')

    reviews_written = db.relationship('Review', foreign_keys='Review.author_id', back_populates='author')
    reviews_received = db.relationship('Review', foreign_keys='Review.target_id', back_populates='target')
    
    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.upjv_id} - {self.email})>"
    
    def to_str(self):
        return f"{self.first_name} {self.last_name}"