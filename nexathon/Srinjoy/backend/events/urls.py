from django.urls import path
from . import views

urlpatterns = [
    # Auth routes
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),

    # Event routes
    path("<str:category>/", views.event_list, name="event_list"),
    path("<str:category>/add/", views.add_event, name="add_event"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
]
