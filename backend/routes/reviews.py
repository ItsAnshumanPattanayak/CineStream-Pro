from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.rating import Rating

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/rate', methods=['POST'])
@login_required
def rate_movie():
    """Rate a movie"""
    data = request.json
    
    # Check if rating already exists
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id,
        movie_id=data['movie_id']
    ).first()
    
    if existing_rating:
        existing_rating.rating = data['rating']
        existing_rating.review = data.get('review')
    else:
        rating = Rating(
            user_id=current_user.id,
            movie_id=data['movie_id'],
            rating=data['rating'],
            review=data.get('review')
        )
        db.session.add(rating)
    
    db.session.commit()
    
    return jsonify({'message': 'Rating saved successfully'}), 201