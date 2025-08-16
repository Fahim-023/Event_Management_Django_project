# events/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # Front page
    path('', views.frontpage, name='frontpage'),

    # Home page with search + category filter
    path('event/home/', views.home, name='home'),

    # Event detail view
    path('event/<int:pk>/', views.event_detail, name='event_detail'),

    # Event CRUD
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:pk>/edit/', views.update_event, name='update_event'),
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),

    # Category CRUD
    path('category/create/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/edit/', views.update_category, name='update_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # User app
    path('users/', include('users.urls')),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin-dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer-dashboard'),
    path('dashboard/participant/', views.participant_dashboard, name='participant-dashboard'),

    # Roles / Groups
    path('create-group/', views.create_group, name='create-group'),
    path('groups/', views.group_list, name='group-list'),
    path('assign-role/<int:user_id>/', views.assign_role, name='assign-role'),
    path('no-permission/', views.no_permission, name='no-permission'),

    # RSVP
    path("event/<int:event_id>/rsvp/", views.rsvp_event, name="rsvp_event"),
]
