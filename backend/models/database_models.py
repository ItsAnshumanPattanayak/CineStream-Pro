from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    interests = db.Column(db.JSON)  # List of genres user is interested in
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'interests': self.interests,
            'created_at': self.created_at.isoformat()
        }


class Movie(db.Model):
    """Movie model"""
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.JSON)  # List of genres
    tags = db.Column(db.JSON)  # List of tags
    director = db.Column(db.String(120))
    cast = db.Column(db.JSON)  # List of actors
    release_date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)  # Duration in minutes
    rating = db.Column(db.Float, default=0.0)  # Average rating
    poster_url = db.Column(db.String(500))
    trailer_url = db.Column(db.String(500))
    streaming_available = db.Column(db.Boolean, default=True)  # Available for online streaming
    language = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('Rating', backref='movie', lazy=True, cascade='all, delete-orphan')
    shows = db.relationship('Theater_Show', backref='movie', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='movie', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'tags': self.tags,
            'director': self.director,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'duration_minutes': self.duration_minutes,
            'rating': self.rating,
            'poster_url': self.poster_url,
            'streaming_available': self.streaming_available,
            'language': self.language
        }
        if include_details:
            data.update({
                'description': self.description,
                'cast': self.cast,
                'trailer_url': self.trailer_url
            })
        return data


class Rating(db.Model):
    """User rating for movies"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)  # 1-5 rating
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating,
            'timestamp': self.timestamp.isoformat()
        }


class Review(db.Model):
    """User review for movies"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'review_text': self.review_text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }


class Theater(db.Model):
    """Theater/Cinema model"""
    __tablename__ = 'theaters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    city = db.Column(db.String(100))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    facilities = db.Column(db.JSON)  # List of facilities
    
    # Relationships
    shows = db.relationship('Theater_Show', backref='theater', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'city': self.city,
            'address': self.address,
            'phone': self.phone,
            'facilities': self.facilities
        }


class Theater_Show(db.Model):
    """Movie show in a theater"""
    __tablename__ = 'theater_shows'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time)
    price_per_ticket = db.Column(db.Float, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    screen_number = db.Column(db.Integer)
    format_type = db.Column(db.String(50))  # 2D, 3D, IMAX
    language = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    seats = db.relationship('Seat', backref='show', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='show', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'theater_id': self.theater_id,
            'show_date': self.show_date.isoformat(),
            'show_time': str(self.show_time),
            'price_per_ticket': self.price_per_ticket,
            'total_seats': self.total_seats,
            'available_seats': self.available_seats,
            'screen_number': self.screen_number,
            'format_type': self.format_type,
            'language': self.language
        }


class Seat(db.Model):
    """Seat in a theater"""
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('theater_shows.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    row = db.Column(db.String(5), nullable=False)
    column = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    seat_type = db.Column(db.String(50))  # Standard, Premium, Recliner
    
    __table_args__ = (db.UniqueConstraint('show_id', 'seat_number', name='unique_show_seat'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'seat_number': self.seat_number,
            'row': self.row,
            'column': self.column,
            'is_available': self.is_available,
            'seat_type': self.seat_type
        }


class Booking(db.Model):
    """Movie booking"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('theater_shows.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled
    total_price = db.Column(db.Float, nullable=False)
    seats_booked = db.Column(db.JSON)  # List of seat IDs
    booking_type = db.Column(db.String(50))  # online_streaming, in_theater, pre_book
    
    # Relationships
    payment = db.relationship('Payment', backref='booking', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'booking_date': self.booking_date.isoformat(),
            'status': self.status,
            'total_price': self.total_price,
            'seats_booked': self.seats_booked,
            'booking_type': self.booking_type
        }


class Payment(db.Model):
    """Payment details"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, debit_card, wallet, etc.
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    transaction_id = db.Column(db.String(100), unique=True)
    payment_date = db.Column(db.DateTime)
    gateway_response = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }
