from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_page, name='services'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/create/', views.booking_create, name='booking_form'),
    path('booking/summary/<int:booking_id>/', views.booking_summary, name='booking_summary'),
    path('booking/confirm/<int:booking_id>/', views.payment_confirm, name='payment_confirm'),
    path('payment/create-order/<int:booking_id>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('chatbot/api/', views.chatbot_view, name='chatbot_api'),
    path('google-login-callback/', views.google_login_callback, name='google_login_callback'),
    path('facebook-login/', views.facebook_login, name='facebook_login'),
    path('facebook-login-callback/', views.facebook_login_callback, name='facebook_login_callback'),
    path('twitter-login/', views.twitter_login, name='twitter_login'),
    path('twitter-login-callback/', views.twitter_login_callback, name='twitter_login_callback'),
    path('review/submit/', views.submit_review, name='submit_review'),
    path('review/approve/<int:review_id>/', views.approve_review, name='approve_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('service/add/', views.add_service, name='add_service'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('gallery/add/', views.add_gallery, name='add_gallery'),
    path('gallery/delete/<int:image_id>/', views.delete_gallery, name='delete_gallery'),
    path('booking/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('booking/manage/<int:booking_id>/', views.manage_booking, name='manage_booking'),
    path('guest/add/<int:booking_id>/', views.add_guest, name='add_guest'),
    path('guest/delete/<int:guest_id>/', views.delete_guest, name='delete_guest'),
    path('guest/checkin/<int:guest_id>/', views.checkin_guest, name='checkin_guest'),
    path('ai-planner/', views.ai_planner, name='ai_planner'),
    path('invitation/create/<int:booking_id>/', views.create_invitation, name='create_invitation'),
    path('invitation/view/<int:booking_id>/', views.view_invitation, name='view_invitation'),
    
    # Admin Panel Sub-modules
    path('admin-panel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/payments/', views.admin_payments, name='admin_payments'),
    path('admin-panel/payments/mark-balance-paid/<int:booking_id>/', views.mark_balance_paid, name='mark_balance_paid'),
    path('admin-panel/payments/update-status/<int:booking_id>/', views.update_payment_status, name='update_payment_status'),
    
    # Service Management
    path('admin-panel/services/', views.admin_services, name='admin_services'),
    path('admin-panel/services/add/', views.add_service, name='add_service'),
    path('admin-panel/services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('admin-panel/services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    
    # Gallery Management
    path('admin-panel/gallery/', views.admin_gallery, name='admin_gallery'),
    path('admin-panel/gallery/add/', views.add_gallery, name='add_gallery'),
    path('admin-panel/gallery/delete/<int:image_id>/', views.delete_gallery, name='delete_gallery'),
    
    # Review Management
    path('admin-panel/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-panel/reviews/approve/<int:review_id>/', views.approve_review, name='approve_review'),
    path('admin-panel/reviews/reject/<int:review_id>/', views.reject_review, name='reject_review'),
    path('admin-panel/reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
