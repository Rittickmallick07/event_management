from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)
EVENT_FILE = "events.json"

# Helper to load/save events
def load_events():
    try:
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_event(event):
    events = load_events()
    events.append(event)
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=4)

@app.route("/", methods=["GET"])
def index():
    events = load_events()
    # Sort by date
    events.sort(key=lambda e: e["event_date"])
    return render_template("index.html", events=events)

@app.route("/add_university_event", methods=["POST"])
def add_event():
    name = request.form.get("event_name")
    date = request.form.get("event_date")  # format yyyy-mm-dd
    location = request.form.get("event_location")
    desc = request.form.get("event_desc")

    if not (name and date and location and desc):
        return "All fields required", 400

    event = {
        "event_name": name,
        "event_date": date,
        "event_location": location,
        "event_desc": desc
    }

    save_event(event)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
