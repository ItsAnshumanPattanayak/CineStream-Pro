import pandas as pd
import os
from extensions import db
from models.movie import Movie
from models.user import User
from models.theater import Theater
from models.show import Show
from datetime import datetime, timedelta
import random

def initialize_database():
    """Initialize database with MovieLens data"""
    
    # Check if already initialized
    if Movie.query.count() > 0:
        print("Database already initialized")
        return
    
    print("Initializing database...")
    
    # Load MovieLens data
    movies_file = 'data/ml-latest-small/movies.csv'
    
    if not os.path.exists(movies_file):
        print(f"MovieLens dataset not found at {movies_file}")
        print("Please download from https://grouplens.org/datasets/movielens/")
        return
    
    movies_df = pd.read_csv(movies_file)
    
    # Populate movies table
    for _, row in movies_df.iterrows():
        title = row['title']
        year = None
        if '(' in title and ')' in title:
            try:
                year = int(title.split('(')[-1].split(')')[0])
                title = title.rsplit('(', 1)[0].strip()
            except:
                pass
        
        movie = Movie(
            movie_id=row['movieId'],
            title=title,
            genres=row['genres'],
            year=year,
            is_streaming=random.choice([True, False]),
            is_in_theaters=random.choice([True, False]),
            poster_url=f"https://via.placeholder.com/300x450?text={title[:20]}"
        )
        db.session.add(movie)
    
    db.session.commit()
    print(f"Loaded {len(movies_df)} movies")
    
    # Create demo users
    if User.query.count() == 0:
        demo_users = [
            {'username': 'demo_user', 'email': 'demo@example.com', 'preferred_genres': 'Action|Thriller'},
            {'username': 'movie_fan', 'email': 'fan@example.com', 'preferred_genres': 'Comedy|Romance'},
        ]
        
        for user_data in demo_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                preferred_genres=user_data['preferred_genres']
            )
            user.set_password('password123')
            db.session.add(user)
        
        db.session.commit()
        print("Created demo users")
    
    # Create sample theaters
    if Theater.query.count() == 0:
        theaters = [
            {'name': 'PVR Cinemas', 'location': 'Downtown', 'city': 'New York'},
            {'name': 'INOX Multiplex', 'location': 'Mall Road', 'city': 'New York'},
        ]
        
        for theater_data in theaters:
            theater = Theater(**theater_data)
            db.session.add(theater)
        
        db.session.commit()
        print("Created theaters")
    
    # Create sample shows
    if Show.query.count() == 0:
        theaters = Theater.query.all()
        in_theater_movies = Movie.query.filter_by(is_in_theaters=True).limit(10).all()
        
        for movie in in_theater_movies:
            for theater in theaters:
                for day in range(7):
                    for hour in [10, 13, 16, 19]:
                        show_time = datetime.now() + timedelta(days=day, hours=hour)
                        show = Show(
                            movie_id=movie.id,
                            theater_id=theater.id,
                            show_time=show_time,
                            screen_number=random.randint(1, 3),
                            price=random.choice([200, 250, 300])
                        )
                        db.session.add(show)
        
        db.session.commit()
        print("Created shows")