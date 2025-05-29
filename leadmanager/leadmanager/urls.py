from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/')),  # Add this line
    path('', include('leads.urls')),  # Make sure this is included
]