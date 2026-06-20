from extensions import db
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200))
    year = db.Column(db.Integer)
    imdb_id = db.Column(db.String(20))
    tmdb_id = db.Column(db.String(20))
    
    # Additional fields
    description = db.Column(db.Text)
    director = db.Column(db.String(100))
    cast = db.Column(db.String(500))
    duration = db.Column(db.Integer)
    language = db.Column(db.String(50))
    poster_url = db.Column(db.String(300))
    trailer_url = db.Column(db.String(300))
    
    # Availability
    is_streaming = db.Column(db.Boolean, default=True)
    is_in_theaters = db.Column(db.Boolean, default=False)
    release_date = db.Column(db.Date)
    
    # Relationships
    ratings = db.relationship('Rating', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    shows = db.relationship('Show', backref='movie', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'title': self.title,
            'genres': self.genres,
            'year': self.year,
            'description': self.description,
            'poster_url': self.poster_url,
            'is_streaming': self.is_streaming,
            'is_in_theaters': self.is_in_theaters
        }