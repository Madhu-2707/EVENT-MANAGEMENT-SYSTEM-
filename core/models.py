from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

class Service(models.Model):
    PACKAGE_CHOICES = [
        ('Budget', 'Budget'),
        ('Standard', 'Standard'),
        ('Luxury', 'Luxury'),
    ]
    name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=20, choices=PACKAGE_CHOICES, default='Standard')
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    price = models.DecimalField(max_digits=10, decimal_places=2) # In ₹

    def __str__(self):
        return f"{self.name} ({self.package_type})"

class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('Wedding', 'Wedding'),
        ('Birthday Party', 'Birthday Party'),
        ('Engagement', 'Engagement'),
        ('Baby Shower', 'Baby Shower'),
        ('Corporate Event', 'Corporate Event'),
        ('Cultural Event', 'Cultural Event'),
        ('Music Concert', 'Music Concert'),
    ]
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.image_hash:
            import hashlib
            hasher = hashlib.sha256()
            for chunk in self.image.chunks():
                hasher.update(chunk)
            self.image_hash = hasher.hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.id}"

class Booking(models.Model):
    EVENT_TYPES = [
        ('Wedding', 'Wedding'),
        ('Birthday', 'Birthday'),
        ('Corporate Event', 'Corporate Event'),
        ('Engagement', 'Engagement'),
        ('Baby Shower', 'Baby Shower'),
        ('College Fest', 'College Fest'),
        ('Anniversary Celebration', 'Anniversary Celebration'),
        ('House Warming Ceremony', 'House Warming Ceremony'),
        ('Product Launch Event', 'Product Launch Event'),
        ('Cultural Events', 'Cultural Events'),
        ('Music Concert Events', 'Music Concert Events'),
    ]
    TIME_SLOTS = [
        ('08:00 - 12:00', 'Morning (8 AM - 12 PM)'),
        ('12:00 - 16:00', 'Afternoon (12 PM - 4 PM)'),
        ('16:00 - 20:00', 'Evening (4 PM - 8 PM)'),
        ('20:00 - 00:00', 'Night (8 PM - 12 AM)'),
    ]
    BUDGET_PACKAGES = [
        ('Luxury', 'Luxury'),
        ('Standard', 'Standard'),
        ('Budget', 'Budget'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_date = models.DateField()
    time_slot = models.CharField(max_length=50, choices=TIME_SLOTS)
    venue = models.CharField(max_length=255) # Stores Venue Name
    venue_address = models.TextField(blank=True, null=True) # Stores Venue Full Address
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    guest_count = models.PositiveIntegerField()
    services = models.ManyToManyField(Service)
    budget_package = models.CharField(max_length=20, choices=BUDGET_PACKAGES)
    
    # Customer Info (Redundant if logged in, but user requested these fields in booking)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20) # Updated for country code + 10 digits
    house_no = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Razorpay Payment Fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    # Payment Tracking
    is_advance_payment = models.BooleanField(default=False)
    is_balance_paid = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    timeline = models.JSONField(blank=True, null=True, help_text="Auto-generated event timeline")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance_amount(self):
        return self.total_price - self.amount_paid

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import uuid
            self.booking_id = str(uuid.uuid4()).split('-')[0].upper()
            
        if not self.timeline and self.status == 'Confirmed':
            self.timeline = self.generate_default_timeline()
            
        super().save(*args, **kwargs)

    def generate_default_timeline(self):
        # Generate a basic timeline based on event type and time slot
        if '12:00' in self.time_slot: # Afternoon
            start = '12:00 PM'
        elif '16:00' in self.time_slot: # Evening
            start = '04:00 PM'
        elif '20:00' in self.time_slot: # Night
            start = '08:00 PM'
        else:
            start = '08:00 AM'
            
        return {
            "Guest Arrival & Welcome Drinks": start,
            "Main Ceremony / Event Start": "1 hour after arrival",
            "Photography Session": "2 hours after arrival",
            "Catering & Dining Starts": "3 hours after arrival",
            "Event Conclusion": "End of slot"
        }

    def __str__(self):
        return f"{self.booking_id} - {self.event_type}"

class Guest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    is_checked_in = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.qr_code:
            import qrcode
            from io import BytesIO
            from django.core.files import File
            import uuid
            
            # Generate QR Code connecting to a check-in endpoint (dummy URL for now)
            qr_data = f"booking:{self.booking.booking_id}|guest:{self.email}|id:{uuid.uuid4()}"
            qr = qrcode.make(qr_data)
            
            fname = f'qr-{self.booking.booking_id}-{self.name}.png'
            buffer = BytesIO()
            qr.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.booking.booking_id}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star – Poor'),
        (2, '2 Stars – Average'),
        (3, '3 Stars – Good'),
        (4, '4 Stars – Very Good'),
        (5, '5 Stars – Excellent'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_approved = models.BooleanField(default=False) # Keep for compatibility, sync with status
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Sync is_approved with status
        if self.status == 'Approved':
            self.is_approved = True
        else:
            self.is_approved = False
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'booking')

    def __str__(self):
        return f"{self.user.email} - {self.booking.booking_id} - {self.rating} Stars"

class Invitation(models.Model):
    TEMPLATE_CHOICES = [
        ('wedding', 'Wedding Theme'),
        ('birthday', 'Birthday Theme'),
        ('corporate', 'Corporate Theme'),
        ('elegant', 'Elegant Theme'),
        ('minimal', 'Minimal Theme'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invitation')
    host_name = models.CharField(max_length=255)
    event_title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.CharField(max_length=100)
    event_venue = models.TextField()
    message = models.TextField(blank=True, null=True)
    template_choice = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='elegant')
    qr_code = models.ImageField(upload_to='invitation_qrs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            import qrcode
            from io import BytesIO
            from django.core.files import File
            
            # Generate QR Code with booking details and venue location
            qr_data = f"Zenvy Events Invitation\nBooking ID: {self.booking.booking_id}\nEvent: {self.event_title}\nVenue: {self.event_venue}"
            qr = qrcode.make(qr_data)
            
            fname = f'inv-qr-{self.booking.booking_id}.png'
            buffer = BytesIO()
            qr.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation for {self.event_title} ({self.booking.booking_id})"
