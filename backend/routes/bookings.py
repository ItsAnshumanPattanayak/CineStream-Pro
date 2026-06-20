from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.booking import Booking
from models.show import Show
from models.seat_layout import SeatLayout
import random
import string
import json

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
@login_required
def get_user_bookings():
    """Get user's booking history"""
    bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.booking_date.desc()).all()
    
    result = []
    for b in bookings:
        booking_dict = b.to_dict()
        booking_dict['movie_title'] = b.show.movie.title
        booking_dict['theater_name'] = b.show.theater.name
        booking_dict['show_time'] = b.show.show_time.isoformat()
        booking_dict['seats'] = json.loads(b.seats)
        result.append(booking_dict)
    
    return jsonify({'bookings': result})

@bookings_bp.route('/book', methods=['POST'])
@login_required
def book_tickets():
    """Book movie tickets"""
    data = request.json
    
    show = Show.query.get_or_404(data['show_id'])
    seat_ids = data['seat_ids']
    
    # Check seat availability
    seats = SeatLayout.query.filter(SeatLayout.id.in_(seat_ids)).all()
    
    for seat in seats:
        if seat.is_booked:
            return jsonify({'error': f'Seat {seat.seat_number} is already booked'}), 400
    
    # Calculate total amount
    TICKET_PRICE = {'normal': 200, 'premium': 350, 'vip': 500}
    total_amount = sum(TICKET_PRICE[s.seat_type] for s in seats)
    
    # Generate booking reference
    booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        show_id=data['show_id'],
        seats=json.dumps([s.seat_number for s in seats]),
        total_amount=total_amount,
        booking_reference=booking_ref,
        payment_status='pending'
    )
    
    db.session.add(booking)
    
    # Mark seats as booked
    for seat in seats:
        seat.is_booked = True
    
    # Update available seats
    show.available_seats -= len(seats)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking_id': booking.id,
        'booking_reference': booking_ref,
        'total_amount': total_amount
    }), 201