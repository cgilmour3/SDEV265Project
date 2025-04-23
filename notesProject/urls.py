from django.contrib import admin
from django.urls import path, include
from notes.views import SignUpView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),  # Include the URLs from the 'notes' app
    path('accounts/', include('django.contrib.auth.urls')), # For user authentication
    path('accounts/signup/', SignUpView.as_view(), name='register'),
]