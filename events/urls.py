from django.urls import path
from . import views

urlpatterns = [
    # Home page with search + category filter
    path('', views.home, name='home'),

    # Event detail view
    path('event/<int:pk>/', views.event_detail, name='event_detail'),

    # Organizer dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Event CRUD
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:pk>/edit/', views.update_event, name='update_event'),
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),

    # Category create
    path('category/create/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    # Category
    path('category/<int:pk>/edit/', views.update_category, name='update_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # Participant create
    path('participant/create/', views.create_participant, name='create_participant'),
    path('participants/', views.participant_list, name='participant_list'),

    # Delete routes
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('participant/<int:pk>/delete/', views.delete_participant, name='delete_participant'),
    # Update routes
    path('category/<int:pk>/edit/', views.update_category, name='update_category'),
    path('participant/<int:pk>/edit/', views.update_participant, name='update_participant'),

]
