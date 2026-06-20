from extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    seats = db.Column(db.String(500))
    total_amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')
    booking_reference = db.Column(db.String(20), unique=True)
    
    # Payment details
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'booking_date': self.booking_date.isoformat(),
            'seats': self.seats,
            'total_amount': self.total_amount,
            'payment_status': self.payment_status,
            'booking_reference': self.booking_reference
        }