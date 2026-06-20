from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.booking import Booking
import random
import string

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/process', methods=['POST'])
@login_required
def process_payment():
    """Process dummy payment"""
    data = request.json
    
    booking = Booking.query.get_or_404(data['booking_id'])
    
    if booking.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Simulate payment processing
    transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    
    booking.payment_status = 'completed'
    booking.payment_method = data.get('payment_method', 'credit_card')
    booking.transaction_id = transaction_id
    
    db.session.commit()
    
    return jsonify({
        'message': 'Payment successful',
        'transaction_id': transaction_id,
        'booking_reference': booking.booking_reference
    })