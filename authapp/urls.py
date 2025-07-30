from django.urls import path, include
from authapp import views

urlpatterns = [
    path('', views.home, name="home"),  # Include the URLs from the auth app
]
 