import string
from app import create_app, db
from app.models import User, Vehicle, Location, Ride, Review
from app.models.ride import reservation_table
from werkzeug.security import generate_password_hash
import random
import os
from datetime import datetime, timedelta
from config import DEV, PROD

app = create_app(config_name=PROD if os.getenv('FLASK_ENV') == 'prod' else DEV)

def seed_users(n=10):
    """Generate n random users."""
    print(f"Seeding {n} users...")
    
    first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"]
    last_names = ["Dupont", "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Owo", "Dubois", "Moreau"]
    
    with app.app_context():
        # Check if users already exist to avoid duplicates if run multiple times
        if User.query.count() > 0:
            print("Users already exist. Skipping seeding.")
            return

        users = []
        for i in range(n):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            upjv_id = f"{random.choice(string.ascii_lowercase)}{random.randint(20000000, 29999999)}"
            email = f"{first_name.lower()}.{last_name.lower()}@etud.u-picardie.fr"
            phone_number = f"06{random.randint(10000000, 99999999)}"
            password = generate_password_hash("password123*")
            
            user = User(
                first_name=first_name,
                last_name=last_name,
                upjv_id=upjv_id,
                email=email,
                phone_number=phone_number,
                password=password
            )
            
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Seeded {n} users!")
        return users

def seed_locations(n=10):
    """Generate n locations."""
    print(f"Seeding {n} locations...")
    
    with app.app_context():
        if Location.query.count() > 0:
            print("Locations already exist. Skipping seeding.")
            return
        
        # Campus and popular locations in Amiens
        locations_data = [
    {
        "name": "Campus UPJV - Citadelle", 
        "lat": 49.9018445, 
        "lon": 2.2966589, 
        "desc": "Campus principal de l'UPJV"
    },
    {
        "name": "Gare d'Amiens", 
        "lat": 49.8904721, 
        "lon": 2.3036325, 
        "desc": "Gare SNCF d'Amiens (Place Alphonse Fiquet)"
    },
    {
        "name": "Centre-ville Amiens", 
        "lat": 49.8934062, 
        "lon": 2.2994828, 
        "desc": "Place Gambetta / Rue des 3 Cailloux"
    },
    {
        "name": "Campus UPJV - Teinturerie", 
        "lat": 49.8887643, 
        "lon": 2.3034952, 
        "desc": "Campus UFR Arts et Sciences"
    },
    {
        "name": "IUT Amiens", 
        "lat": 49.8730987, 
        "lon": 2.2741954, 
        "desc": "IUT d'Amiens (Avenue des Facultés)"
    },
    {
        "name": "Pôle Jules Verne", 
        "lat": 49.8647221, 
        "lon": 2.3698115, 
        "desc": "Zone commerciale Grand A (Glisy)"
    },
    {
        "name": "Hôpital Nord", 
        "lat": 49.9102451, 
        "lon": 2.3197853, 
        "desc": "Ancien site CHU Amiens-Picardie"
    },
    {
        "name": "Parc Saint-Pierre", 
        "lat": 49.8980312, 
        "lon": 2.3113345, 
        "desc": "Parc urbain et étang"
    },
    {
        "name": "Cathédrale d'Amiens", 
        "lat": 49.8947678, 
        "lon": 2.3023021, 
        "desc": "Notre-Dame d'Amiens"
    },
    {
        "name": "Université - Pôle Santé", 
        "lat": 49.8755013, 
        "lon": 2.2778005, 
        "desc": "CHU Amiens-Sud / Campus Santé"
    }
]
        
        locations = []
        for loc_data in locations_data[:n]:
            location = Location(**loc_data)
            db.session.add(location)
            locations.append(location)
        
        db.session.commit()
        print(f"Seeded {len(locations)} locations!")
        return locations

def seed_vehicles(users, ratio=0.6):
    """Generate vehicles for a ratio of users."""
    print(f"Seeding vehicles for {int(len(users) * ratio)} users...")
    
    with app.app_context():
        if Vehicle.query.count() > 0:
            print("Vehicles already exist. Skipping seeding.")
            return
        
        models = ["Peugeot 208", "Renault Clio", "Citroën C3", "Volkswagen Golf", "Ford Fiesta", 
                  "Toyota Yaris", "Opel Corsa", "Fiat 500", "Mini Cooper", "Audi A3"]
        colors = ["Blanc", "Noir", "Gris", "Rouge", "Bleu", "Vert", "Argent"]
        
        vehicles = []
        # Give vehicles to a subset of users
        users_with_vehicles = random.sample(users, int(len(users) * ratio))
        
        for user in users_with_vehicles:
            # Generate unique license plate
            license_plate = f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}-{random.randint(100, 999)}-{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
            
            vehicle = Vehicle(
                model=random.choice(models),
                color=random.choice(colors),
                licence_plate=license_plate,
                max_seats=random.randint(3, 5),
                owner_id=user.id
            )
            
            db.session.add(vehicle)
            vehicles.append(vehicle)
        
        db.session.commit()
        print(f"Seeded {len(vehicles)} vehicles!")
        return vehicles

def seed_rides(users, locations, n=20):
    """Generate n rides."""
    print(f"Seeding {n} rides...")
    
    with app.app_context():
        if Ride.query.count() > 0:
            print("Rides already exist. Skipping seeding.")
            return
        
        # Only users with vehicles can be drivers
        users_with_vehicles = [user for user in users if user.vehicle is not None]
        
        if not users_with_vehicles:
            print("No users with vehicles. Cannot create rides.")
            return []
        
        rides = []
        now = datetime.utcnow()
        
        for i in range(n):
            driver = random.choice(users_with_vehicles)
            start_loc = random.choice(locations)
            end_loc = random.choice([loc for loc in locations if loc.id != start_loc.id])
            
            # Random date within next 30 days
            days_ahead = random.randint(0, 30)
            hours_ahead = random.randint(0, 23)
            ride_date = now + timedelta(days=days_ahead, hours=hours_ahead)
            
            ride = Ride(
                date=ride_date,
                seats=random.randint(1, driver.vehicle.max_seats - 1),  # At least 1 seat available
                driver_id=driver.id,
                start_location_id=start_loc.id,
                end_location_id=end_loc.id
            )
            
            db.session.add(ride)
            rides.append(ride)
        
        db.session.commit()
        print(f"Seeded {len(rides)} rides!")
        return rides

def seed_reservations(rides, users, avg_passengers=2):
    """Add passengers to rides."""
    print(f"Seeding reservations...")
    
    with app.app_context():
        reservation_count = 0
        for ride in rides:
            # Don't book passengers on rides with no available seats
            if not ride.seats or ride.seats <= 0:
                continue

            # Random number of passengers (but not more than available seats)
            num_passengers = random.randint(0, min(ride.seats, avg_passengers))

            # Get users who are not the driver and not already passengers
            potential_passengers = [user for user in users if user.id != ride.driver_id]
            if not potential_passengers or num_passengers == 0:
                continue

            passengers = random.sample(potential_passengers, min(num_passengers, len(potential_passengers)))

            # Insert into association table explicitly to ensure rows in `reservation`
            for p in passengers:
                # Avoid duplicate entries
                existing = db.session.execute(
                    reservation_table.select().where(
                        (reservation_table.c.user_id == p.id) & (reservation_table.c.ride_id == ride.id)
                    )
                ).first()
                if existing:
                    continue
                db.session.execute(
                    reservation_table.insert().values(user_id=p.id, ride_id=ride.id)
                )
                reservation_count += 1

        db.session.commit()
        print(f"Seeded {reservation_count} reservations!")

def seed_reviews(rides, ratio=0.5):
    """Generate reviews for completed rides."""
    print(f"Seeding reviews...")
    
    with app.app_context():
        if Review.query.count() > 0:
            print("Reviews already exist. Skipping seeding.")
            return
        
        reviews = []
        now = datetime.utcnow()

        # Only review rides that are in the past
        past_rides = [ride for ride in rides if ride.date < now]
        
        # Review a subset of past rides
        rides_to_review = random.sample(past_rides, min(int(len(past_rides) * ratio), len(past_rides)))
        
        comments = [
            "Super trajet, conducteur très sympa !",
            "Ponctuel et agréable, je recommande.",
            "Voiture propre, conduite sûre.",
            "Belle expérience, à refaire.",
            "RAS, tout s'est bien passé.",
            "Conducteur bavard mais sympathique.",
            "Trajet rapide et efficace.",
            "Merci pour le covoiturage !",
            "Conduite un peu sportive mais ça va.",
            "Parfait, rien à redire."
        ]
        
        for ride in rides_to_review:
            # Passengers review the driver
            for passenger in ride.passengers:
                review = Review(
                    content=random.choice(comments),
                    rating=random.randint(3, 5),  # Most reviews are positive
                    ride_id=ride.id,
                    author_id=passenger.id,
                    target_id=ride.driver_id
                )
                db.session.add(review)
                reviews.append(review)
            
            # Sometimes driver reviews passengers too
            if random.random() < 0.3 and ride.passengers:  # 30% chance
                passenger_to_review = random.choice(ride.passengers)
                review = Review(
                    content=random.choice(comments),
                    rating=random.randint(3, 5),
                    ride_id=ride.id,
                    author_id=ride.driver_id,
                    target_id=passenger_to_review.id
                )
                db.session.add(review)
                reviews.append(review)
        
        db.session.commit()
        print(f"Seeded {len(reviews)} reviews!")
        return reviews

def seed_all():
    """Seed all data in order."""
    print("Starting database seeding...")
    
    with app.app_context():
        users = seed_users(n=15)
        
    with app.app_context():
        # Re-query users to get them in this context
        users = User.query.all()
        locations = seed_locations(n=10)
        
    with app.app_context():
        users = User.query.all()
        vehicles = seed_vehicles(users, ratio=0.6)
        
    with app.app_context():
        users = User.query.all()
        locations = Location.query.all()
        rides = seed_rides(users, locations, n=20)
        
    with app.app_context():
        rides = Ride.query.all()
        users = User.query.all()
        seed_reservations(rides, users, avg_passengers=2)
        
    with app.app_context():
        rides = Ride.query.all()
        seed_reviews(rides, ratio=0.5)
    
    print("\n✅ Database seeding complete!")

if __name__ == "__main__":
    seed_all()
