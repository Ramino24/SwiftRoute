import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_backend.settings')
django.setup()

from core.models import Booking, Trip
from django.contrib.auth import get_user_model

User = get_user_model()

def seed_data():
    trips = Trip.objects.all()
    users = User.objects.all()
    
    if not trips or not users:
        print("Make sure you have at least one Trip and one User created first!")
        return

    print("Generating historical bookings for SwiftRoute...")
    
    for _ in range(200):
        random_trip = random.choice(trips)
        random_user = random.choice(users)
        
        # Determine the price
        # Check if price is on the trip, or the route, otherwise default to 5000
        trip_price = getattr(random_trip, 'price', 
                     getattr(random_trip.route, 'price', 5000))
        
        days_ago = random.randint(0, 30)
        random_date = timezone.now() - timedelta(days=days_ago)
        
        Booking.objects.create(
            user=random_user,
            trip=random_trip,
            payment_status='successful',
            price=trip_price, # Using the fallback logic here
            payment_reference=f"SEED-{random.getrandbits(32)}",
            seat_count=random.randint(1, 4),
            created_at=random_date
        )
    print("Successfully seeded 200 historical bookings!")

if __name__ == "__main__":
    seed_data()