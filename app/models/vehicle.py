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
    
    def __repr__(self):
        return f"<Vehicle {self.model} ({self.licence_plate}) owned by User ID {self.owner_id}>"
    
    def is_valid(self) -> bool:
        return all([
            self.model,
            self.licence_plate,
            isinstance(self.max_seats, int) and self.max_seats > 0
        ])