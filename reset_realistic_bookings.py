import os
import django
import sys
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

# Add the project directory to sys.path
sys.path.append(r'c:\Users\mahas\Desktop\janani')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from core.models import Booking, User

def cleanup_and_populate_realistic_data():
    # Get the admin user
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("No staff user found. Please create one first.")
            return
    except Exception as e:
        print(f"Error fetching admin user: {e}")
        return

    # 1. DELETE ALL EXISTING BOOKINGS to reset revenue
    print("Deleting all existing bookings to reset revenue...")
    Booking.objects.all().delete()

    # 2. DEFINED REALISTIC DUMMY DATA (Last 5 Months Trend)
    today = timezone.now()
    
    dummy_data = [
        # Current Month (March 2026 approx)
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
        },
        # Last Month (Feb 2026)
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
            'created_at_offset': 30
        },
        # Jan 2026
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
            'created_at_offset': 60
        },
        # Dec 2025
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
            'created_at_offset': 90
        },
        # Nov 2025
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
            'created_at_offset': 120
        },
         # Another one for trend
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
            'created_at_offset': 45
        },
    ]

    for data in dummy_data:
        offset = data.pop('created_at_offset', 0)
        # We can't set created_at in .create() for auto_now_add=True fields easily without mocking or update
        # But for charts in views.py, they filter by created_at
        try:
            booking = Booking.objects.create(
                user=admin_user,
                guest_count=100,
                time_slot='12:00 - 16:00',
                is_advance_payment=True,
                **data
            )
            if offset > 0:
                # Update created_at using .update() to bypass auto_now_add
                Booking.objects.filter(id=booking.id).update(created_at=today - timedelta(days=offset))
            print(f"Created realistic booking {booking.booking_id}")
        except Exception as e:
            print(f"Error creating booking {data['booking_id']}: {e}")

    # Final Revenue Calculation check
    total = Booking.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    print(f"Total Revenue now: ₹{total}")

if __name__ == '__main__':
    cleanup_and_populate_realistic_data()
