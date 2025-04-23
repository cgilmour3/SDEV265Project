from django.urls import path
from . import views

app_name = 'notes'  # For namespacing your URLs

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('create/', views.note_create, name='note_create'),
    path('<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('signup/', views.SignUpView.as_view(), name='register'),
     path('logout/', views.logout_view, name='logout'), 
]