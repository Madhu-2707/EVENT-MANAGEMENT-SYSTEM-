from django.contrib import admin
from .models import User, Service, Gallery, Booking, Review, Invitation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'is_staff')

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'host_name', 'booking', 'template_choice')
    list_filter = ('template_choice', 'event_type')
    search_fields = ('event_title', 'host_name', 'booking__booking_id')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_filter = ('category',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'event_type', 'event_date', 'status', 'total_price')
    list_filter = ('status', 'event_type')
    search_fields = ('booking_id', 'customer_email', 'customer_name')
