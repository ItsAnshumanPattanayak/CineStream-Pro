from flask import Blueprint, request, jsonify
from app import db
from models.database_models import Review, Movie
from routes.auth import token_required
from datetime import datetime

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/create', methods=['POST'])
@token_required
def create_review(current_user):
    """Create a movie review"""
    try:
        data = request.get_json()
        
        movie_id = data.get('movie_id')
        review_text = data.get('review_text')
        rating = data.get('rating')
        
        if not movie_id or not review_text:
            return jsonify({'message': 'Missing movie_id or review_text'}), 400
        
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        # Check if user already reviewed this movie
        existing_review = Review.query.filter_by(
            user_id=current_user.id,
            movie_id=movie_id
        ).first()
        
        if existing_review:
            # Update existing review
            existing_review.review_text = review_text
            existing_review.rating = rating
            existing_review.updated_at = datetime.utcnow()
        else:
            # Create new review
            review = Review(
                user_id=current_user.id,
                movie_id=movie_id,
                review_text=review_text,
                rating=rating
            )
            db.session.add(review)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review saved successfully',
            'review': (existing_review or review).to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie_reviews(movie_id):
    """Get all reviews for a movie"""
    try:
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        sort_by = request.args.get('sort_by', 'recent')  # recent, helpful
        
        query = Review.query.filter_by(movie_id=movie_id)
        
        # Sort
        if sort_by == 'recent':
            query = query.order_by(Review.created_at.desc())
        elif sort_by == 'rating':
            query = query.order_by(Review.rating.desc())
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        reviews = []
        for review in paginated.items:
            review_dict = review.to_dict()
            review_dict['user'] = {
                'id': review.user.id,
                'username': review.user.username,
                'first_name': review.user.first_name
            }
            reviews.append(review_dict)
        
        return jsonify({
            'movie_id': movie_id,
            'reviews': reviews,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Get specific review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'message': 'Review not found'}), 404
        
        review_dict = review.to_dict()
        review_dict['user'] = {
            'id': review.user.id,
            'username': review.user.username,
            'first_name': review.user.first_name
        }
        review_dict['movie'] = review.movie.to_dict()
        
        return jsonify({
            'review': review_dict
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@token_required
def update_review(current_user, review_id):
    """Update a review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'message': 'Review not found'}), 404
        
        if review.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'review_text' in data:
            review.review_text = data['review_text']
        if 'rating' in data:
            review.rating = data['rating']
        
        review.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@token_required
def delete_review(current_user, review_id):
    """Delete a review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'message': 'Review not found'}), 404
        
        if review.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/user/all', methods=['GET'])
@token_required
def get_user_reviews(current_user):
    """Get all reviews by current user"""
    try:
        reviews = Review.query.filter_by(user_id=current_user.id).order_by(
            Review.created_at.desc()
        ).all()
        
        result = []
        for review in reviews:
            review_dict = review.to_dict()
            review_dict['movie'] = review.movie.to_dict()
            result.append(review_dict)
        
        return jsonify({
            'reviews': result,
            'total': len(result)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@reviews_bp.route('/stats/<int:movie_id>', methods=['GET'])
def get_review_statistics(movie_id):
    """Get review statistics for a movie"""
    try:
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        reviews = Review.query.filter_by(movie_id=movie_id).all()
        
        if not reviews:
            return jsonify({
                'movie_id': movie_id,
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {}
            }), 200
        
        # Calculate statistics
        ratings = [r.rating for r in reviews if r.rating]
        
        # Rating distribution
        distribution = {}
        for i in range(1, 6):
            count = sum(1 for r in reviews if r.rating == i)
            distribution[str(i)] = count
        
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return jsonify({
            'movie_id': movie_id,
            'total_reviews': len(reviews),
            'average_rating': avg_rating,
            'rating_distribution': distribution,
            'recent_reviews': [r.to_dict() for r in reviews[-5:]]
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
