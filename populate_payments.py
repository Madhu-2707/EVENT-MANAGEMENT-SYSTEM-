import os
import django
import sys
from decimal import Decimal
from datetime import date

# Add the project directory to sys.path
sys.path.append(r'c:\Users\mahas\Desktop\janani')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Booking, User

def populate_dummy_payments():
    # Get the admin user
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("No staff user found. Please create one first.")
            return
    except Exception as e:
        print(f"Error fetching admin user: {e}")
        return

    # Clear existing dummy bookings if they have specific IDs we're about to use
    booking_ids = ['BKG001', 'BKG002', 'BKG003', 'BKG004', 'BKG005', 'BKG006', 'BKG007', 'BKG008']
    Booking.objects.filter(booking_id__in=booking_ids).delete()

    dummy_data = [
        {
            'booking_id': 'BKG001',
            'customer_name': 'Rahul Sharma',
            'event_type': 'Wedding',
            'budget_package': 'Luxury',
            'total_price': Decimal('120000'),
            'amount_paid': Decimal('5000'),
            'status': 'Pending',
            'event_date': date(2026, 4, 20),
            'customer_email': 'rahul@example.com',
            'customer_phone': '9876543210',
            'venue': 'Royal Palace',
            'guest_count': 500,
            'time_slot': '08:00 - 12:00',
            'is_advance_payment': True,
            'is_balance_paid': False
        },
        {
            'booking_id': 'BKG002',
            'customer_name': 'Priya Menon',
            'event_type': 'Birthday',
            'budget_package': 'Budget',
            'total_price': Decimal('25000'),
            'amount_paid': Decimal('5000'),
            'status': 'Pending',
            'event_date': date(2026, 5, 18),
            'customer_email': 'priya@example.com',
            'customer_phone': '9876543211',
            'venue': 'Garden Boutique',
            'guest_count': 50,
            'time_slot': '16:00 - 20:00',
            'is_advance_payment': True,
            'is_balance_paid': False
        },
        {
            'booking_id': 'BKG003',
            'customer_name': 'Arjun Kumar',
            'event_type': 'Engagement',
            'budget_package': 'Standard',
            'total_price': Decimal('60000'),
            'amount_paid': Decimal('5000'),
            'status': 'Pending',
            'event_date': date(2026, 6, 12),
            'customer_email': 'arjun@example.com',
            'customer_phone': '9876543212',
            'venue': 'Blue Lagoon Resort',
            'guest_count': 150,
            'time_slot': '12:00 - 16:00',
            'is_advance_payment': True,
            'is_balance_paid': False
        },
        {
            'booking_id': 'BKG004',
            'customer_name': 'Sneha Patel',
            'event_type': 'Corporate Event',
            'budget_package': 'Luxury',
            'total_price': Decimal('150000'),
            'amount_paid': Decimal('150000'),
            'status': 'Confirmed',
            'event_date': date(2026, 7, 25),
            'customer_email': 'sneha@example.com',
            'customer_phone': '9876543213',
            'venue': 'Grand Hyatt',
            'guest_count': 200,
            'time_slot': '08:00 - 12:00',
            'is_advance_payment': True,
            'is_balance_paid': True
        },
        {
            'booking_id': 'BKG005',
            'customer_name': 'Karthik Reddy',
            'event_type': 'Baby Shower',
            'budget_package': 'Standard',
            'total_price': Decimal('45000'),
            'amount_paid': Decimal('5000'),
            'status': 'Pending',
            'event_date': date(2026, 8, 15),
            'customer_email': 'karthik@example.com',
            'customer_phone': '9876543214',
            'venue': 'Greenwood Hall',
            'guest_count': 80,
            'time_slot': '16:00 - 20:00',
            'is_advance_payment': True,
            'is_balance_paid': False
        },
        {
            'booking_id': 'BKG006',
            'customer_name': 'Anjali Verma',
            'event_type': 'Cultural Event',
            'budget_package': 'Budget',
            'total_price': Decimal('20000'),
            'amount_paid': Decimal('20000'),
            'status': 'Completed',
            'event_date': date(2026, 9, 30),
            'customer_email': 'anjali@example.com',
            'customer_phone': '9876543215',
            'venue': 'City Auditorium',
            'guest_count': 300,
            'time_slot': '12:00 - 16:00',
            'is_advance_payment': True,
            'is_balance_paid': True
        },
        {
            'booking_id': 'BKG007',
            'customer_name': 'Vikram Singh',
            'event_type': 'Wedding',
            'budget_package': 'Luxury',
            'total_price': Decimal('200000'),
            'amount_paid': Decimal('50000'),
            'status': 'Confirmed',
            'event_date': date(2026, 11, 10),
            'customer_email': 'vikram@example.com',
            'customer_phone': '9876543216',
            'venue': 'Imperial Palace',
            'guest_count': 600,
            'time_slot': '16:00 - 20:00',
            'is_advance_payment': True,
            'is_balance_paid': False
        },
        {
            'booking_id': 'BKG008',
            'customer_name': 'Meera Joshi',
            'event_type': 'Engagement',
            'budget_package': 'Standard',
            'total_price': Decimal('55000'),
            'amount_paid': Decimal('55000'),
            'status': 'Completed',
            'event_date': date(2025, 12, 25),
            'customer_email': 'meera@example.com',
            'customer_phone': '9876543217',
            'venue': 'Skyline Hotel',
            'guest_count': 120,
            'time_slot': '20:00 - 00:00',
            'is_advance_payment': True,
            'is_balance_paid': True
        },
    ]

    for data in dummy_data:
        try:
            booking = Booking.objects.create(
                user=admin_user,
                **data
            )
            print(f"Created booking {booking.booking_id}")
        except Exception as e:
            print(f"Error creating booking {data['booking_id']}: {e}")

if __name__ == '__main__':
    populate_dummy_payments()
