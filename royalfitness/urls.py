from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("authapp.urls")),  # Include the URLs from the auth app
]
 