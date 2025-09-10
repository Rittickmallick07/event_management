from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    path("api/events/", views.event_list, name="event_list"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),                        # homepage → event list
    path("events/", views.event_list, name="event_list"),      # list all events
    path("events/add/", views.add_event, name="add_event"),    # add new event
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),  # event details
]
