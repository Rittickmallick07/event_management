import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Event
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime

def event_to_dict(ev):
    d = model_to_dict(ev)
    # format datetime ISO
    d['date'] = ev.date.isoformat()
    return d

def list_events(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    events = Event.objects.order_by("date").all()
    data = [event_to_dict(ev) for ev in events]
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_event(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = json.loads(request.body.decode("utf-8"))
        name = payload.get("name")
        date = payload.get("date")
        description = payload.get("description", "")
        if not name or not date:
            return HttpResponseBadRequest("Missing name or date")
        # parse date; accept ISO or datetime-local like "2025-09-01T12:00"
        dt = parse_datetime(date)
        if dt is None:
            # try replacing space with T
            dt = parse_datetime(date.replace(" ", "T"))
        if dt is None:
            return HttpResponseBadRequest("Invalid date format")
        ev = Event.objects.create(name=name, description=description, date=dt)
        return JsonResponse(event_to_dict(ev), status=201)
    except Exception as e:
        return HttpResponseBadRequest(str(e))


@csrf_exempt
def delete_event(request, ev_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    try:
        ev = Event.objects.filter(id=ev_id)
        if not ev.exists():
            return JsonResponse({"error": "Not found"}, status=404)
        ev.delete()
        return JsonResponse({"ok": True})
    except Exception as e:
        return HttpResponseBadRequest(str(e))
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_collection, name='events_collection'),   # GET and POST
    path('<int:ev_id>/', views.delete_event, name='delete_event'), # DELETE
]
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Event
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime

def event_to_dict(ev):
    d = model_to_dict(ev)
    d['date'] = ev.date.isoformat()
    return d

@csrf_exempt
def events_collection(request):
    if request.method == "GET":
        events = Event.objects.order_by("date").all()
        data = [event_to_dict(ev) for ev in events]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
            name = payload.get("name")
            date = payload.get("date")
            description = payload.get("description", "")
            if not name or not date:
                return HttpResponseBadRequest("Missing name or date")
            dt = parse_datetime(date)
            if dt is None:
                dt = parse_datetime(date.replace(" ", "T"))
            if dt is None:
                return HttpResponseBadRequest("Invalid date format")
            ev = Event.objects.create(name=name, description=description, date=dt)
            return JsonResponse(event_to_dict(ev), status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@csrf_exempt
def delete_event(request, ev_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])
    try:
        ev = Event.objects.filter(id=ev_id)
        if not ev.exists():
            return JsonResponse({"error": "Not found"}, status=404)
        ev.delete()
        return JsonResponse({"ok": True})
    except Exception as e:
        return HttpResponseBadRequest(str(e))
# events/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json
from .models import Event

def index(request):
    return render(request, "events/index.html")

def event_list(request):
    """Return all events as JSON."""
    events = Event.objects.all().order_by("date")
    data = [
        {
            "id": e.id,
            "name": e.name,
            "date": e.date.isoformat(),
            "location": e.location,
            "description": e.description,
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def add_event(request):
    """Add new event via POST (AJAX)."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            date = parse_datetime(data.get("date"))
            location = data.get("location")
            description = data.get("description", "")

            event = Event.objects.create(
                name=name, date=date, location=location, description=description
            )
            return JsonResponse({
                "id": event.id,
                "name": event.name,
                "date": event.date.isoformat(),
                "location": event.location,
                "description": event.description,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)
from django.shortcuts import render, get_object_or_404
from .models import Event

# List of all events
def event_list(request):
    events = Event.objects.all().order_by("date")
    return render(request, "events/event_list.html", {"events": events})

# Event details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, "events/event_list.html", {"events": events})

def add_event(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        date = request.POST["date"]
        location = request.POST["location"]

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location
        )
        return redirect("event_list")
