
from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('', views.Home, name='Home'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('contact', views.contact, name='contact'),
    path('join', views.enroll, name='enroll'),
    path('profile', views.profile, name='profile'),
    path('gallery',views.gallery,name="gallery"),
    path('attendance',views.attendance,name="attendance"),
    path('about/',views.about,name="about"),
    path('services/',views.services,name="services"),
    path('payment/<int:order_id>',views.payment, name="payment"),
    path('payment-success/<int:order_id>', views.payment_success, name="payment-success"),
    path('free-trial/', views.free_trial, name='free_trial'),
    
    # ... other URL patterns
    path('join/', views.enroll, name='join'),
    path('initiate-payment/', views.initiate_payment, name='initiate-payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
