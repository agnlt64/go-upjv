from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
import random

app = create_app()

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

        for i in range(n):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            upjv_id = f"{random.randint(20000000, 29999999)}"
            email = f"{first_name.lower()}.{last_name.lower()}{i}@etud.u-picardie.fr"
            phone_number = f"06{random.randint(10000000, 99999999)}"
            password = generate_password_hash("password123")
            
            user = User(
                first_name=first_name,
                last_name=last_name,
                upjv_id=upjv_id,
                email=email,
                phone_number=phone_number,
                password=password
            )
            
            db.session.add(user)
        
        db.session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_users()
