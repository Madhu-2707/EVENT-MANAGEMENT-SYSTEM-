import os
import django
import sys
from datetime import date, timedelta
from django.utils import timezone

# Add the project directory to sys.path
sys.path.append(r'c:\Users\mahas\Desktop\janani')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Booking, User, Review

def populate_dummy_reviews():
    # Ensure we have a staff user and some bookings
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("No staff user found.")
        return

    # Delete existing reviews to start fresh
    print("Cleaning up old reviews...")
    Review.objects.all().delete()

    # Get some bookings to link reviews to
    bookings = list(Booking.objects.all())
    if not bookings:
        print("No bookings found. Please run reset_realistic_bookings.py first.")
        return

    dummy_reviews = [
        {
            'customer_name': 'Priya Sharma',
            'event_type': 'Wedding',
            'rating': 5,
            'comment': "The wedding decoration and catering were excellent. Everything was organized perfectly.",
            'status': 'Approved',
            'days_ago': 3
        },
        {
            'customer_name': 'Rahul Kumar',
            'event_type': 'Birthday',
            'rating': 4,
            'comment': "The birthday party setup was beautiful and the DJ service was very good.",
            'status': 'Approved',
            'days_ago': 5
        },
        {
            'customer_name': 'Sneha Patel',
            'event_type': 'Corporate Event',
            'rating': 5,
            'comment': "Very professional planning and smooth event management. Highly satisfied.",
            'status': 'Approved',
            'days_ago': 2
        },
        {
            'customer_name': 'Arjun Reddy',
            'event_type': 'Engagement',
            'rating': 4,
            'comment': "The stage decoration and lighting were really attractive. Great work by the team.",
            'status': 'Pending',
            'days_ago': 1
        },
        {
            'customer_name': 'Divya Menon',
            'event_type': 'Baby Shower',
            'rating': 5,
            'comment': "The decoration theme was lovely and all arrangements were handled nicely.",
            'status': 'Approved',
            'days_ago': 4
        },
        {
            'customer_name': 'Karthik S',
            'event_type': 'Cultural Events',
            'rating': 4,
            'comment': "The sound system and stage setup were impressive. Overall, a good experience.",
            'status': 'Pending',
            'days_ago': 0
        },
    ]

    for i, data in enumerate(dummy_reviews):
        # Find a booking that matches the event type if possible, or just cycle through
        booking = bookings[i % len(bookings)]
        
        # We need a user for the review. We can use the admin or create dummy users.
        # For simplicity, I'll use the admin user but override the display name in the template if needed, 
        # or better, create dummy users.
        
        dummy_email = f"user_{i}@example.com"
        user, created = User.objects.get_or_create(
            email=dummy_email, 
            defaults={'username': dummy_email.split('@')[0], 'name': data['customer_name']}
        )
        
        review = Review.objects.create(
            user=user,
            booking=booking,
            rating=data['rating'],
            comment=data['comment'],
            status=data['status']
        )
        
        # Set created_at
        if data['days_ago'] > 0:
            Review.objects.filter(id=review.id).update(created_at=timezone.now() - timedelta(days=data['days_ago']))
            
        print(f"Created review from {data['customer_name']} - {data['status']}")

    print("Dummy reviews population complete.")

if __name__ == '__main__':
    populate_dummy_reviews()
