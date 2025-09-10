from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save message to DB
            return render(request, "contact_success.html")  # Success page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
from django.shortcuts import render, redirect
from .models import Event
from django.utils import timezone

def add_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        description = request.POST.get("description")
        Event.objects.create(name=name, date=date, description=description)
        return redirect("add_event")  # stay on same page after adding
    events = Event.objects.all().order_by("date")
    return render(request, "events/add_event.html", {"events": events})
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UniversityEvent

def add_university_event(request):
    if request.method == "POST":
        name = request.POST['event_name']
        date = request.POST['event_date']
        location = request.POST['event_location']
        desc = request.POST['event_desc']
        UniversityEvent.objects.create(
            name=name, date=date, location=location, description=desc
        )
        return HttpResponse("✅ Event Saved Successfully!")
    return render(request, "university.html")
from django.db import models

class UniversityEvent(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
from django.shortcuts import render, redirect
from .models import UniversityEvent
from .forms import UniversityEventForm

def university_events(request):
    events = UniversityEvent.objects.all().order_by("date")
    return render(request, "university_events.html", {"events": events})

def add_university_event(request):
    if request.method == "POST":
        form = UniversityEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("university_events")
    else:
        form = UniversityEventForm()
    return render(request, "add_university_event.html", {"form": form})
from django.shortcuts import render, redirect
from .models import ConferenceEvent
from django.utils import timezone

def conference_events(request):
    if request.method == "POST":
        name = request.POST.get("event_name")
        date = request.POST.get("event_date")
        location = request.POST.get("event_location")
        desc = request.POST.get("event_desc")

        ConferenceEvent.objects.create(
            name=name, date=date, location=location, description=desc
        )
        return redirect("conference_events")

    events = ConferenceEvent.objects.all().order_by("date")
    return render(request, "events/conferences.html", {"events": events})
from django.shortcuts import render, redirect
from .models import ConferenceEvent
from django.utils import timezone

def conferences(request):
    if request.method == "POST":
        name = request.POST.get("event_name")
        date = request.POST.get("event_date")
        location = request.POST.get("event_location")
        desc = request.POST.get("event_desc")

        ConferenceEvent.objects.create(
            name=name,
            date=date,
            location=location,
            description=desc
        )
        return redirect("conferences")

    events = ConferenceEvent.objects.filter(date__gte=timezone.now()).order_by("date")
    return render(request, "events/conferences.html", {"events": events})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Login View
def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # redirect to dashboard/home
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")
    return render(request, "events/login.html")


# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "events/signup.html")


# Logout View
def user_logout(request):
    logout(request)
    return redirect("/")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Conference Events Page (Protected)
@login_required(login_url="/events/login/")
def conferences(request):
    if request.method == "POST":
        # You can connect this to your Event model later
        event_name = request.POST.get("event_name")
        event_date = request.POST.get("event_date")
        event_location = request.POST.get("event_location")
        event_desc = request.POST.get("event_desc")
        messages.success(request, f"Conference '{event_name}' saved successfully!")
        return redirect("conferences")

    return render(request, "events/conferences.html")


# University Events Page (Protected)
@login_required(login_url="/events/login/")
def university_events(request):
    if request.method == "POST":
        event_name = request.POST.get("event_name")
        event_date = request.POST.get("event_date")
        event_location = request.POST.get("event_location")
        event_desc = request.POST.get("event_desc")
        messages.success(request, f"University Event '{event_name}' saved successfully!")
        return redirect("university_events")

    return render(request, "events/university.html")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event

# Add Conference
@login_required(login_url="/events/login/")
def conferences(request):
    if request.method == "POST":
        Event.objects.create(
            name=request.POST.get("event_name"),
            event_type="conference",
            date=request.POST.get("event_date"),
            location=request.POST.get("event_location"),
            description=request.POST.get("event_desc"),
            created_by=request.user
        )
        messages.success(request, "✅ Conference added successfully!")
        return redirect("conferences")

    events = Event.objects.filter(event_type="conference").order_by("date")
    return render(request, "events/conferences.html", {"events": events})


# Add University Event
@login_required(login_url="/events/login/")
def university_events(request):
    if request.method == "POST":
        Event.objects.create(
            name=request.POST.get("event_name"),
            event_type="university",
            date=request.POST.get("event_date"),
            location=request.POST.get("event_location"),
            description=request.POST.get("event_desc"),
            created_by=request.user
        )
        messages.success(request, "✅ University event added successfully!")
        return redirect("university_events")

    events = Event.objects.filter(event_type="university").order_by("date")
    return render(request, "events/university.html", {"events": events})
from django.shortcuts import render, redirect
from .models import UniversityEvent

def university_events(request):
    if request.method == "POST":
        name = request.POST["event_name"]
        date = request.POST["event_date"]
        location = request.POST["event_location"]
        desc = request.POST["event_desc"]

        UniversityEvent.objects.create(
            name=name, date=date, location=location, description=desc
        )
        return redirect("university_events")

    events = UniversityEvent.objects.all()
    return render(request, "university_events.html", {"events": events})
from django.shortcuts import render, redirect
from .models import UniversityEvent
from django.utils import timezone

def university_events(request):
    events = UniversityEvent.objects.all().order_by("date")
    return render(request, "university_events.html", {"events": events})

def add_university_event(request):
    if request.method == "POST":
        name = request.POST["event_name"]
        date = request.POST["event_date"]
        location = request.POST["event_location"]
        desc = request.POST["event_desc"]

        UniversityEvent.objects.create(
            name=name,
            date=date,
            location=location,
            description=desc
        )
        return redirect("university_events")

    return redirect("university_events")
from django.shortcuts import render
from django.http import JsonResponse
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by("date")
    data = [
        {
            "id": e.id,
            "name": e.name,
            "date": e.date.strftime("%Y-%m-%d %H:%M:%S"),
            "location": e.location,
            "description": e.description,
        }
        for e in events
    ]
    return JsonResponse(data, safe=False)

def index(request):
    return render(request, "events/index.html")
from django.shortcuts import render, redirect
from .models import Event
from django.utils import timezone

def event_list(request, category):
    events = Event.objects.filter(category=category, date__gte=timezone.now()).order_by("date")
    return render(request, "events/event_list.html", {"events": events, "category": category})

def add_event(request, category):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        date = request.POST["date"]  # will be YYYY-MM-DDTHH:MM from input
        location = request.POST["location"]

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            category=category
        )
        return redirect("event_list", category=category)
    return render(request, "events/add_event.html", {"category": category})
def event_list(request, category):
    events = Event.objects.filter(category=category).order_by("date")
    return render(request, "events/event_list.html", {"events": events, "category": category})
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Event


# ========== AUTH VIEWS ==========

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "events/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("event_list", category="university")  # default redirect
    else:
        form = AuthenticationForm()
    return render(request, "events/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


# ========== EVENT VIEWS ==========

def event_list(request, category):
    """Show upcoming events filtered by category."""
    events = Event.objects.filter(
        category=category,
        date__gte=timezone.now()
    ).order_by("date")
    return render(request, "events/event_list.html", {"events": events, "category": category})


def event_detail(request, event_id):
    """Show details for a single event."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})


def add_event(request, category):
    """Allow users to add an event in a specific category."""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")  # HTML datetime-local field gives ISO format
        location = request.POST.get("location")

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            category=category,
            created_by=request.user if request.user.is_authenticated else None
        )
        return redirect("event_list", category=category)

    return render(request, "events/add_event.html", {"category": category})
