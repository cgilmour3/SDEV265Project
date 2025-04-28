from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', include('notes.urls')),
    path('', RedirectView.as_view(url='/notes/', permanent=True)), 
    path('users/', include('users.urls')),
]
