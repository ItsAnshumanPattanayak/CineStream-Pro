from flask import Blueprint, request, jsonify
from app import db
from models.database_models import Payment, Booking, User
from routes.auth import token_required
from datetime import datetime
import uuid
import json

payments_bp = Blueprint('payments', __name__)


def generate_transaction_id():
    """Generate a unique transaction ID"""
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def process_dummy_payment(payment_method, amount, card_details=None):
    """
    Simulate payment processing
    Returns success/failure based on mock logic
    """
    # Mock payment validation
    valid_methods = ['credit_card', 'debit_card', 'wallet', 'upi']
    
    if payment_method not in valid_methods:
        return False, 'Invalid payment method'
    
    # Mock credit card validation (demo purposes only)
    if payment_method in ['credit_card', 'debit_card']:
        if not card_details:
            return False, 'Card details required'
        
        # Simple mock validation
        card_number = card_details.get('card_number', '')
        if len(card_number) != 16 or not card_number.isdigit():
            return False, 'Invalid card number'
        
        cvv = card_details.get('cvv', '')
        if len(cvv) != 3 or not cvv.isdigit():
            return False, 'Invalid CVV'
    
    # Mock success (90% success rate)
    import random
    if random.random() > 0.1:  # 90% success
        return True, 'Payment processed successfully'
    else:
        return False, 'Payment gateway error'


@payments_bp.route('/process', methods=['POST'])
@token_required
def process_payment(current_user):
    """Process payment for a booking"""
    try:
        data = request.get_json()
        
        booking_id = data.get('booking_id')
        payment_method = data.get('payment_method')
        card_details = data.get('card_details')
        
        if not booking_id or not payment_method:
            return jsonify({'message': 'Missing booking_id or payment_method'}), 400
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Check if payment already exists
        if booking.payment:
            return jsonify({'message': 'Payment already processed for this booking'}), 400
        
        # Process payment
        success, message = process_dummy_payment(payment_method, booking.total_price, card_details)
        
        # Create payment record
        payment = Payment(
            booking_id=booking_id,
            amount=booking.total_price,
            payment_method=payment_method,
            transaction_id=generate_transaction_id(),
            status='completed' if success else 'failed',
            payment_date=datetime.utcnow() if success else None,
            gateway_response={
                'success': success,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        db.session.add(payment)
        
        # Update booking status if payment successful
        if success:
            booking.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'payment': payment.to_dict(),
            'booking_status': booking.status,
            'success': success
        }), 200 if success else 402
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/<int:payment_id>', methods=['GET'])
@token_required
def get_payment(current_user, payment_id):
    """Get payment details"""
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'message': 'Payment not found'}), 404
        
        # Check if user owns this booking
        if payment.booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        return jsonify({
            'payment': payment.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/booking/<int:booking_id>', methods=['GET'])
@token_required
def get_booking_payment(current_user, booking_id):
    """Get payment for a specific booking"""
    try:
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        
        if booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        payment = booking.payment
        
        if not payment:
            return jsonify({
                'message': 'No payment found for this booking',
                'booking_id': booking_id
            }), 404
        
        return jsonify({
            'payment': payment.to_dict(),
            'booking': booking.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/validate-card', methods=['POST'])
def validate_card():
    """Validate card details (dummy validation)"""
    try:
        data = request.get_json()
        
        card_number = data.get('card_number', '')
        cvv = data.get('cvv', '')
        expiry = data.get('expiry', '')
        
        errors = []
        
        # Validate card number (Luhn algorithm - simplified)
        if len(card_number) != 16 or not card_number.isdigit():
            errors.append('Card number must be 16 digits')
        
        # Validate CVV
        if len(cvv) != 3 or not cvv.isdigit():
            errors.append('CVV must be 3 digits')
        
        # Validate expiry
        if not expiry or '/' not in expiry:
            errors.append('Expiry format should be MM/YY')
        else:
            try:
                month, year = expiry.split('/')
                if not (1 <= int(month) <= 12):
                    errors.append('Invalid month')
            except:
                errors.append('Invalid expiry format')
        
        if errors:
            return jsonify({
                'valid': False,
                'errors': errors
            }), 400
        
        return jsonify({
            'valid': True,
            'message': 'Card details are valid'
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/refund/<int:payment_id>', methods=['POST'])
@token_required
def refund_payment(current_user, payment_id):
    """Process refund for a payment"""
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'message': 'Payment not found'}), 404
        
        if payment.booking.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        if payment.status != 'completed':
            return jsonify({'message': 'Can only refund completed payments'}), 400
        
        # Update payment status
        payment.status = 'refunded'
        payment.gateway_response['refund_timestamp'] = datetime.utcnow().isoformat()
        
        # Update booking status
        payment.booking.status = 'refunded'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Refund processed successfully',
            'payment': payment.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/user/history', methods=['GET'])
@token_required
def get_payment_history(current_user):
    """Get payment history for current user"""
    try:
        # Get all payments for user's bookings
        payments = db.session.query(Payment).join(Booking).filter(
            Booking.user_id == current_user.id
        ).order_by(Payment.created_at.desc()).all()
        
        result = []
        for payment in payments:
            payment_dict = payment.to_dict()
            payment_dict['booking'] = payment.booking.to_dict()
            payment_dict['movie'] = payment.booking.show.movie.to_dict()
            result.append(payment_dict)
        
        return jsonify({
            'payments': result,
            'total': len(result),
            'total_spent': sum(p.amount for p in payments if p.status == 'completed')
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@payments_bp.route('/stats', methods=['GET'])
def get_payment_statistics():
    """Get payment statistics (admin endpoint)"""
    try:
        total_payments = Payment.query.count()
        completed_payments = Payment.query.filter_by(status='completed').count()
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(
            status='completed'
        ).scalar() or 0
        
        payment_methods = db.session.query(
            Payment.payment_method,
            db.func.count(Payment.id).label('count'),
            db.func.sum(Payment.amount).label('total')
        ).filter_by(status='completed').group_by(
            Payment.payment_method
        ).all()
        
        methods = {}
        for method, count, total in payment_methods:
            methods[method] = {'count': count, 'total': total}
        
        return jsonify({
            'total_payments': total_payments,
            'completed_payments': completed_payments,
            'total_revenue': float(total_revenue),
            'payment_methods': methods
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
