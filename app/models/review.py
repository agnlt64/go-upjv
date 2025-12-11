from app import db

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    ride = db.relationship('Ride', back_populates='reviews')
    
    # Comme il y a deux FK vers User, on doit dire à SQLAlchemy laquelle utiliser
    author = db.relationship('User', foreign_keys=[author_id], back_populates='reviews_written')
    target = db.relationship('User', foreign_keys=[target_id], back_populates='reviews_received')