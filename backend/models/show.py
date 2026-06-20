from extensions import db
from datetime import datetime

class Show(db.Model):
    __tablename__ = 'shows'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), nullable=False)
    show_time = db.Column(db.DateTime, nullable=False)
    screen_number = db.Column(db.Integer)
    total_seats = db.Column(db.Integer, default=120)
    available_seats = db.Column(db.Integer, default=120)
    price = db.Column(db.Float, default=200.0)
    
    # Relationships
    bookings = db.relationship('Booking', backref='show', lazy='dynamic', cascade='all, delete-orphan')
    seats = db.relationship('SeatLayout', backref='show', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'theater_id': self.theater_id,
            'show_time': self.show_time.isoformat(),
            'screen_number': self.screen_number,
            'total_seats': self.total_seats,
            'available_seats': self.available_seats,
            'price': self.price
        }