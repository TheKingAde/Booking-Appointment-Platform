from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import sqlite3
import json
import requests
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Telegram Bot Configuration
TG_API_URL = "https://api.telegram.org"
BOT_TOKEN = "7969763015:AAEliO2m1l9Yn7dDY8j_PKvG3_4yHlXbuZY"
CHAT_ID = "6126141848"

# Database Models
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Telegram notification function
def send_telegram_notification(message):
    try:
        url = f"{TG_API_URL}/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/booking')
def booking():
    services = Service.query.all()
    return render_template('booking.html', services=services)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (in production, use proper hashing)
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    bookings = Booking.query.order_by(Booking.appointment_date.desc()).all()
    return render_template('admin_dashboard.html', bookings=bookings)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# API Endpoints
@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'duration': s.duration,
        'price': s.price,
        'description': s.description
    } for s in services])

@app.route('/api/available-slots', methods=['GET'])
def get_available_slots():
    service_id = request.args.get('service_id')
    date = request.args.get('date')
    
    if not service_id or not date:
        return jsonify({'error': 'Service ID and date are required'}), 400
    
    try:
        selected_date = datetime.strptime(date, '%Y-%m-%d')
        service = Service.query.get(service_id)
        
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        # Generate available time slots (9 AM to 6 PM)
        slots = []
        current_time = selected_date.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = selected_date.replace(hour=18, minute=0, second=0, microsecond=0)
        
        while current_time < end_time:
            # Check if this slot is already booked
            existing_booking = Booking.query.filter_by(
                service_id=service_id,
                appointment_date=current_time
            ).first()
            
            if not existing_booking:
                slots.append({
                    'time': current_time.strftime('%H:%M'),
                    'datetime': current_time.isoformat(),
                    'available': True
                })
            
            current_time += timedelta(minutes=service.duration)
        
        return jsonify({'slots': slots})
    
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    required_fields = ['client_name', 'client_email', 'client_phone', 'service_id', 'appointment_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        appointment_date = datetime.fromisoformat(data['appointment_date'])
        
        # Check if slot is still available
        existing_booking = Booking.query.filter_by(
            service_id=data['service_id'],
            appointment_date=appointment_date
        ).first()
        
        if existing_booking:
            return jsonify({'error': 'Time slot is no longer available'}), 400
        
        # Create new booking
        booking = Booking(
            client_name=data['client_name'],
            client_email=data['client_email'],
            client_phone=data['client_phone'],
            service_id=data['service_id'],
            appointment_date=appointment_date,
            notes=data.get('notes', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Send Telegram notification
        service = Service.query.get(data['service_id'])
        message = f"""
🎉 <b>New Booking Confirmed!</b>

👤 <b>Client:</b> {data['client_name']}
📧 <b>Email:</b> {data['client_email']}
📞 <b>Phone:</b> {data['client_phone']}
💼 <b>Service:</b> {service.name}
📅 <b>Date:</b> {appointment_date.strftime('%Y-%m-%d')}
🕐 <b>Time:</b> {appointment_date.strftime('%H:%M')}
💰 <b>Price:</b> ${service.price}
📝 <b>Notes:</b> {data.get('notes', 'None')}

Booking ID: #{booking.id}
        """
        
        send_telegram_notification(message)
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking_id': booking.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
@admin_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()
    
    if 'appointment_date' in data:
        try:
            booking.appointment_date = datetime.fromisoformat(data['appointment_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    if 'status' in data:
        booking.status = data['status']
    
    db.session.commit()
    
    # Send Telegram notification about update
    message = f"""
📝 <b>Booking Updated!</b>

Booking ID: #{booking.id}
👤 <b>Client:</b> {booking.client_name}
📅 <b>New Date:</b> {booking.appointment_date.strftime('%Y-%m-%d %H:%M')}
📋 <b>Status:</b> {booking.status}
    """
    
    send_telegram_notification(message)
    
    return jsonify({'message': 'Booking updated successfully'})

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Send Telegram notification about cancellation
    message = f"""
❌ <b>Booking Cancelled!</b>

Booking ID: #{booking.id}
👤 <b>Client:</b> {booking.client_name}
📅 <b>Date:</b> {booking.appointment_date.strftime('%Y-%m-%d %H:%M')}
💼 <b>Service:</b> {booking.service.name}
    """
    
    send_telegram_notification(message)
    
    db.session.delete(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample services if none exist
        if not Service.query.first():
            sample_services = [
                Service(name='Hair Cut & Style', duration=60, price=45.00, description='Professional haircut and styling'),
                Service(name='Manicure & Pedicure', duration=90, price=35.00, description='Complete nail care service'),
                Service(name='Facial Treatment', duration=75, price=65.00, description='Rejuvenating facial treatment'),
                Service(name='Massage Therapy', duration=60, price=80.00, description='Relaxing full-body massage'),
                Service(name='Consultation', duration=30, price=25.00, description='Initial consultation session')
            ]
            
            for service in sample_services:
                db.session.add(service)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)