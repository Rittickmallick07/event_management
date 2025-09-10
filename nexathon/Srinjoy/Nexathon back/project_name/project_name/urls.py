from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='list_events'),           # GET /api/events/
    path('', views.create_event, name='create_event'),         # POST /api/events/
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_collection, name='events_collection'),   # GET, POST
    path('<int:ev_id>/', views.delete_event, name='delete_event'), # DELETE
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("university-events/", include("events.urls")),
]
from django.urls import path, include

urlpatterns = [
    path("events/", include("events.urls")),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),  # All event + auth routes
]
