import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

from core.models import User, Service, Booking, Review
from django.utils import timezone
import datetime

# Create an admin user if not exists
if not User.objects.filter(email='admin@demo.com').exists():
    admin = User.objects.create_superuser(username='admin@demo.com', email='admin@demo.com', password='adminpass', name='Admin Master')
else:
    admin = User.objects.get(email='admin@demo.com')

# Create a normal user
if not User.objects.filter(email='user@demo.com').exists():
    user = User.objects.create_user(username='user@demo.com', email='user@demo.com', password='userpass', name='John Demo')
else:
    user = User.objects.get(email='user@demo.com')

# Create some services
s1, _ = Service.objects.get_or_create(name='Premium Wedding Package', defaults={'description': 'A full luxury wedding.', 'price': 500000})
s2, _ = Service.objects.get_or_create(name='Corporate Annual Gala', defaults={'description': 'End of year corporate event.', 'price': 250000})

# Create some bookings
b1, _ = Booking.objects.get_or_create(
    user=user, 
    event_type='Wedding', 
    event_date=timezone.now().date() + datetime.timedelta(days=10),
    time_slot='16:00 - 22:00',
    venue='Grand Hotel',
    guest_count=200,
    budget_package='Gold',
    customer_phone='1234567890',
    customer_address='123 Main St',
    defaults={'total_price': 500000, 'status': 'Completed'}
)

b2, _ = Booking.objects.get_or_create(
    user=user, 
    event_type='Corporate Event', 
    event_date=timezone.now().date() - datetime.timedelta(days=5),
    time_slot='10:00 - 16:00',
    venue='City Convention Center',
    guest_count=500,
    budget_package='Platinum',
    customer_phone='1234567890',
    customer_address='123 Main St',
    defaults={'total_price': 250000, 'status': 'Completed'}
)

# Add services to bookings
b1.services.add(s1)
b2.services.add(s2)

# Create Reviews
Review.objects.get_or_create(
    user=user,
    booking=b1,
    defaults={'rating': 5, 'comment': 'Absolutely fantastic wedding service! The decor and catering were top notch.', 'is_approved': True}
)

Review.objects.get_or_create(
    user=user,
    booking=b2,
    defaults={'rating': 4, 'comment': 'Great corporate event setup. Everything was smooth, though the mic had a slight delay.', 'is_approved': True}
)

print("Dummy data added successfully!")
