from flask import Blueprint, request, jsonify
from extensions import db
from models.movie import Movie
from models.rating import Rating
import random

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized recommendations"""
    # Simple recommendation: popular movies the user hasn't rated
    rated_movies = db.session.query(Rating.movie_id).filter_by(user_id=user_id).all()
    rated_ids = [r[0] for r in rated_movies]
    
    # Get popular movies
    popular = db.session.query(
        Movie.id,
        db.func.avg(Rating.rating).label('avg_rating'),
        db.func.count(Rating.id).label('count')
    ).join(Rating).filter(
        Movie.id.notin_(rated_ids) if rated_ids else True
    ).group_by(Movie.id).having(
        db.func.count(Rating.id) >= 5
    ).order_by(
        db.desc('avg_rating')
    ).limit(20).all()
    
    recommendations = []
    for movie_id, avg_rating, count in popular:
        movie = Movie.query.get(movie_id)
        if movie:
            movie_dict = movie.to_dict()
            movie_dict['predicted_score'] = avg_rating
            recommendations.append(movie_dict)
    
    return jsonify({'recommendations': recommendations})

@recommendations_bp.route('/similar/<int:movie_id>', methods=['GET'])
def get_similar_movies(movie_id):
    """Get similar movies based on genre"""
    movie = Movie.query.get_or_404(movie_id)
    
    if not movie.genres:
        return jsonify({'similar_movies': []})
    
    # Find movies with similar genres
    similar = Movie.query.filter(
        Movie.id != movie_id,
        Movie.genres.contains(movie.genres.split('|')[0])
    ).limit(10).all()
    
    return jsonify({
        'similar_movies': [m.to_dict() for m in similar]
    })