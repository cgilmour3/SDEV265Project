from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', include('notes.urls')), # Consider if this is the best place
    path('', RedirectView.as_view(url='/notes/', permanent=True)), # Add this line
]