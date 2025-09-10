from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    datetime_iso = db.Column(db.String(50), nullable=False)  # ISO string
    location = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'university' or 'sports'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'datetime_iso': self.datetime_iso,
            'location': self.location,
            'category': self.category
        }

# On first run, ensure DB exists
@app.before_first_request
def create_tables():
    db.create_all()

# Simple demo login (replace in production)
VALID_USER = {
    'email': 'admin@example.com',
    'password': 'password123'  # demo only
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        if email == VALID_USER['email'] and password == VALID_USER['password']:
            session['user'] = email
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials (demo account).', 'danger')
    return render_template('index.html')  # login appears on top of main page for this UI

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/')
def index():
    # show events grouped by category
    university_events = Event.query.filter_by(category='university').order_by(Event.datetime_iso).all()
    sports_events = Event.query.filter_by(category='sports').order_by(Event.datetime_iso).all()
    return render_template('index.html',
                           university_events=university_events,
                           sports_events=sports_events,
                           user=session.get('user'))

@app.route('/add_event', methods=['POST'])
def add_event():
    # Accepts university events (category param for flexibility)
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    # Expect a datetime-local input (YYYY-MM-DDTHH:MM). If the user provided just date, append T00:00
    dt = request.form.get('datetime') or request.form.get('date') or ''
    if 'T' not in dt and dt:
        # date-only -> make midnight
        dt = f"{dt}T00:00"
    location = request.form.get('location', '').strip()
    category = request.form.get('category', 'university')

    if not (title and description and dt and location):
        flash('Please fill all event fields.', 'warning')
        return redirect(url_for('index'))

    # store ISO format
    try:
        # Validate
        parsed = datetime.fromisoformat(dt)
        iso = parsed.isoformat()
    except Exception:
        flash('Invalid date/time format.', 'danger')
        return redirect(url_for('index'))

    event = Event(title=title, description=description, datetime_iso=iso, location=location, category=category)
    db.session.add(event)
    db.session.commit()
    flash('Event added.', 'success')
    return redirect(url_for('index'))

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('index'))

# optional JSON API for client-side usage
@app.route('/api/events')
def api_events():
    evs = Event.query.order_by(Event.datetime_iso).all()
    return jsonify([e.to_dict() for e in evs])

if __name__ == '__main__':
    app.run(debug=True)
