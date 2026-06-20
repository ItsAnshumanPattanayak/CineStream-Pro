from flask import Blueprint, request, jsonify
from app import db
from models.database_models import (
    Booking, Theater_Show, Seat, User, Movie, Payment
)
from routes.auth import token_required
from datetime import datetime
import random
import string

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/create', methods=['POST'])
@token_required
def create_booking(current_user):
    """Create a new movie booking"""
    try:
        data = request.get_json()
        
        show_id = data.get('show_id')
        seat_ids = data.get('seat_ids', [])
        booking_type = data.get('booking_type', 'in_theater')  # in_theater, pre_book, online_streaming
        
        if not show_id or not seat_ids:
            return jsonify({'message': 'Missing show_id or seat_ids'}), 400
        
        show = Theater_Show.query.get(show_id)
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        
        # Verify seats are available
        seats = Seat.query.filter(
            Seat.show_id == show_id,
            Seat.id.in_(seat_ids)
        ).all()
        
        if len(seats) != len(seat_ids):
            return jsonify({'message': 'Some seats not found'}), 404
        
        for seat in seats:
            if not seat.is_available:
                return jsonify({'message': f'Seat {seat.seat_number} is not available'}), 400
        
        # Calculate total price
        total_price = show.price_per_ticket * len(seats)
        
        # Create booking
        booking = Booking(
            user_id=current_user.id,
            show_id=show_id,
            total_price=total_price,
            seats_booked=[s.id for s in seats],
            booking_type=booking_type,
            status='pending'  # Will be confirmed after payment
        )
        
        db.session.add(booking)
        db.session.flush()  # Get booking id
        
        # Mark seats as unavailable
        for seat in seats:
            seat.is_available = False
        
        # Update available seats count
        show.available_seats -= len(seats)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict(),
            'seats': [s.to_dict() for s in seats],
            'payment_required': total_price
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@token_required
def cancel_booking(current_user, booking_id):
    """Cancel a booking and free up seats"""
    try:
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        if booking.status == 'cancelled':
            return jsonify({'message': 'Booking already cancelled'}), 400
        
        # Free up seats
        if booking.seats_booked:
            seats = Seat.query.filter(Seat.id.in_(booking.seats_booked)).all()
            for seat in seats:
                seat.is_available = True
            
            # Update available seats count
            booking.show.available_seats += len(seats)
        
        booking.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@token_required
def get_booking(current_user, booking_id):
    """Get booking details"""
    try:
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Get show and movie details
        show = booking.show
        movie = show.movie
        theater = show.theater
        
        # Get booked seats
        seats = Seat.query.filter(Seat.id.in_(booking.seats_booked)).all()
        
        return jsonify({
            'booking': booking.to_dict(),
            'movie': movie.to_dict(),
            'show': show.to_dict(),
            'theater': theater.to_dict(),
            'seats': [s.to_dict() for s in seats],
            'payment': booking.payment.to_dict() if booking.payment else None
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/user/all', methods=['GET'])
@token_required
def get_user_bookings(current_user):
    """Get all bookings for current user"""
    try:
        status = request.args.get('status')
        booking_type = request.args.get('booking_type')
        
        query = Booking.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        if booking_type:
            query = query.filter_by(booking_type=booking_type)
        
        bookings = query.order_by(Booking.booking_date.desc()).all()
        
        result = []
        for booking in bookings:
            booking_data = booking.to_dict()
            booking_data['movie'] = booking.show.movie.to_dict()
            booking_data['show'] = booking.show.to_dict()
            booking_data['theater'] = booking.show.theater.to_dict()
            result.append(booking_data)
        
        return jsonify({
            'bookings': result,
            'total': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/<int:show_id>/seats', methods=['GET'])
def get_show_seats(show_id):
    """Get all seats for a show with availability status"""
    try:
        show = Theater_Show.query.get(show_id)
        
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        
        seats = Seat.query.filter_by(show_id=show_id).order_by(
            Seat.row.asc(),
            Seat.column.asc()
        ).all()
        
        # Group seats by row
        seats_by_row = {}
        for seat in seats:
            if seat.row not in seats_by_row:
                seats_by_row[seat.row] = []
            seats_by_row[seat.row].append(seat.to_dict())
        
        return jsonify({
            'show_id': show_id,
            'total_seats': show.total_seats,
            'available_seats': show.available_seats,
            'seats': seats_by_row
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/pre-book', methods=['POST'])
@token_required
def pre_book_movie(current_user):
    """Pre-book a movie (for future shows)"""
    try:
        data = request.get_json()
        show_id = data.get('show_id')
        
        if not show_id:
            return jsonify({'message': 'Missing show_id'}), 400
        
        show = Theater_Show.query.get(show_id)
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        
        # Create booking with pre_book status
        booking = Booking(
            user_id=current_user.id,
            show_id=show_id,
            total_price=0,  # Price not yet determined
            booking_type='pre_book',
            status='pending'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Pre-booking created successfully',
            'booking': booking.to_dict(),
            'movie': show.movie.to_dict(),
            'show': show.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@bookings_bp.route('/<int:booking_id>/upgrade-to-paid', methods=['POST'])
@token_required
def upgrade_to_paid(current_user, booking_id):
    """Upgrade pre-booking to paid booking with seat selection"""
    try:
        data = request.get_json()
        seat_ids = data.get('seat_ids', [])
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        if booking.booking_type != 'pre_book':
            return jsonify({'message': 'Booking is not a pre-booking'}), 400
        
        if not seat_ids:
            return jsonify({'message': 'No seats selected'}), 400
        
        # Verify and reserve seats
        seats = Seat.query.filter(
            Seat.show_id == booking.show_id,
            Seat.id.in_(seat_ids)
        ).all()
        
        if len(seats) != len(seat_ids):
            return jsonify({'message': 'Some seats not found'}), 404
        
        for seat in seats:
            if not seat.is_available:
                return jsonify({'message': f'Seat {seat.seat_number} is not available'}), 400
        
        # Update booking
        booking.seats_booked = [s.id for s in seats]
        booking.total_price = booking.show.price_per_ticket * len(seats)
        
        # Mark seats as unavailable
        for seat in seats:
            seat.is_available = False
        
        booking.show.available_seats -= len(seats)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Pre-booking upgraded successfully',
            'booking': booking.to_dict(),
            'payment_required': booking.total_price
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
