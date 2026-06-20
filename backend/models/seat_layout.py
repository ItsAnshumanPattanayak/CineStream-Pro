from extensions import db

class SeatLayout(db.Model):
    __tablename__ = 'seat_layouts'
    
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    seat_number = db.Column(db.String(10))
    seat_type = db.Column(db.String(20))
    is_booked = db.Column(db.Boolean, default=False)
    row = db.Column(db.String(5))
    column = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'show_id': self.show_id,
            'seat_number': self.seat_number,
            'seat_type': self.seat_type,
            'is_booked': self.is_booked,
            'row': self.row,
            'column': self.column
        }