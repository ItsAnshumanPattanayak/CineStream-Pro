from flask import Blueprint, request, jsonify
from app import db
from models.database_models import User, Movie, Rating, Theater_Show, Booking
from routes.auth import token_required
from ml_models.recommendation_engine import RecommendationEngine
import json

recommendations_bp = Blueprint('recommendations', __name__)

# Initialize recommendation engine
rec_engine = RecommendationEngine()


def prepare_recommendation_data():
    """Prepare data for recommendation engine"""
    # Get all ratings
    ratings = Rating.query.all()
    ratings_data = [{
        'user_id': r.user_id,
        'movie_id': r.movie_id,
        'rating': r.rating
    } for r in ratings]
    
    # Get all movies
    movies = Movie.query.all()
    movies_data = [{
        'id': m.id,
        'title': m.title,
        'genre': m.genre or [],
        'tags': m.tags or []
    } for m in movies]
    
    return ratings_data, movies_data


@recommendations_bp.route('/personalized', methods=['GET'])
@token_required
def get_personalized_recommendations(current_user):
    """Get personalized recommendations for current user"""
    try:
        n = request.args.get('n', 5, type=int)
        method = request.args.get('method', 'hybrid')  # hybrid, user_user, item_item, content, mf
        
        # Prepare data
        ratings_data, movies_data = prepare_recommendation_data()
        
        if not ratings_data:
            # Return popular movies if no ratings
            popular = db.session.query(Movie).order_by(
                Movie.rating.desc()
            ).limit(n).all()
            return jsonify({
                'recommendations': [m.to_dict() for m in popular],
                'method': 'popular',
                'reason': 'No ratings data available yet'
            }), 200
        
        # Build matrices
        rec_engine.build_user_item_matrix(ratings_data)
        rec_engine.build_content_features(movies_data)
        
        # Get recommendations based on method
        if method == 'user_user':
            rec_ids = rec_engine.collaborative_filtering_user_user(current_user.id, n)
        elif method == 'item_item':
            rec_ids = rec_engine.collaborative_filtering_item_item(current_user.id, n)
        elif method == 'content':
            # Get first rated movie for content-based filtering
            first_rated = db.session.query(Rating).filter_by(
                user_id=current_user.id
            ).first()
            if first_rated:
                rec_ids = rec_engine.content_based_filtering(first_rated.movie_id, n)
            else:
                rec_ids = []
        elif method == 'mf':
            rec_engine.matrix_factorization(n_factors=10)
            rec_ids = rec_engine.recommend_using_mf(current_user.id, n)
        else:  # hybrid
            rec_ids = rec_engine.hybrid_recommendations(current_user.id, n_recommendations=n)
        
        # Fetch movie details
        recommendations = []
        for movie_id in rec_ids:
            movie = Movie.query.get(movie_id)
            if movie:
                recommendations.append(movie.to_dict())
        
        return jsonify({
            'recommendations': recommendations,
            'method': method,
            'count': len(recommendations)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/by-interest', methods=['GET'])
@token_required
def get_recommendations_by_interest(current_user):
    """Get recommendations based on user's interests"""
    try:
        n = request.args.get('n', 5, type=int)
        
        if not current_user.interests:
            return jsonify({
                'message': 'User has no interests set. Update your profile first.'
            }), 400
        
        # Query movies matching user interests
        recommendations = []
        for interest in current_user.interests:
            movies = Movie.query.filter(
                Movie.genre.contains(interest)
            ).order_by(Movie.rating.desc()).limit(n).all()
            recommendations.extend(movies)
        
        # Remove duplicates and limit
        seen = set()
        unique_recs = []
        for movie in recommendations:
            if movie.id not in seen:
                seen.add(movie.id)
                unique_recs.append(movie)
        
        return jsonify({
            'recommendations': [m.to_dict() for m in unique_recs[:n]],
            'interests': current_user.interests
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/similar-to/<int:movie_id>', methods=['GET'])
def get_similar_movies(movie_id):
    """Get movies similar to given movie"""
    try:
        n = request.args.get('n', 5, type=int)
        
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        # Prepare data
        ratings_data, movies_data = prepare_recommendation_data()
        
        if not movies_data:
            return jsonify({
                'message': 'No movies available'
            }), 404
        
        # Build content features
        rec_engine.build_content_features(movies_data)
        
        # Get similar movies
        similar_ids = rec_engine.content_based_filtering(movie_id, n)
        
        # Fetch movie details
        similar_movies = []
        for sim_id in similar_ids:
            if sim_id < len(movies_data):
                sim_movie = Movie.query.get(sim_id)
                if sim_movie:
                    similar_movies.append(sim_movie.to_dict())
        
        return jsonify({
            'original_movie': movie.to_dict(),
            'similar_movies': similar_movies
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/trending', methods=['GET'])
def get_trending_recommendations():
    """Get trending movies"""
    try:
        n = request.args.get('n', 10, type=int)
        
        # Get movies with highest recent ratings
        from datetime import datetime, timedelta
        recent_date = datetime.utcnow() - timedelta(days=7)
        
        trending = db.session.query(
            Movie,
            db.func.count(Rating.id).label('rating_count'),
            db.func.avg(Rating.rating).label('avg_rating')
        ).join(Rating).filter(
            Rating.timestamp >= recent_date
        ).group_by(Movie.id).order_by(
            db.func.count(Rating.id).desc()
        ).limit(n).all()
        
        result = []
        for movie, count, avg_rating in trending:
            movie_dict = movie.to_dict()
            movie_dict['recent_ratings'] = count
            result.append(movie_dict)
        
        return jsonify({
            'trending_movies': result
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/popular', methods=['GET'])
def get_popular_recommendations():
    """Get popular movies"""
    try:
        n = request.args.get('n', 10, type=int)
        
        popular = Movie.query.order_by(Movie.rating.desc()).limit(n).all()
        
        return jsonify({
            'popular_movies': [m.to_dict() for m in popular]
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/watched', methods=['GET'])
@token_required
def get_watched_recommendations(current_user):
    """Get recommendations based on user's watched/rated movies"""
    try:
        n = request.args.get('n', 5, type=int)
        
        # Get user's top-rated movies
        user_ratings = Rating.query.filter_by(
            user_id=current_user.id
        ).order_by(Rating.rating.desc()).limit(3).all()
        
        if not user_ratings:
            return jsonify({
                'message': 'User has not rated any movies yet'
            }), 400
        
        # Get similar movies
        recommendations = set()
        for rating in user_ratings:
            similar = Movie.query.filter(
                Movie.genre.contains(Movie.query.get(rating.movie_id).genre[0])
            ).order_by(Movie.rating.desc()).limit(n).all()
            recommendations.update([m.id for m in similar])
        
        # Exclude user's already rated movies
        rated_movie_ids = {r.movie_id for r in user_ratings}
        recommendations = [m for m in recommendations if m not in rated_movie_ids]
        
        # Fetch movie details
        movies = [Movie.query.get(mid) for mid in list(recommendations)[:n]]
        
        return jsonify({
            'recommendations': [m.to_dict() for m in movies if m],
            'based_on': len(user_ratings)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@recommendations_bp.route('/evaluate', methods=['POST'])
def evaluate_recommendations():
    """Evaluate recommendation accuracy (for testing)"""
    try:
        # Get test ratings
        ratings = Rating.query.all()
        test_ratings = [{
            'user_id': r.user_id,
            'movie_id': r.movie_id,
            'rating': r.rating
        } for r in ratings]
        
        if not test_ratings:
            return jsonify({
                'message': 'No ratings data available for evaluation'
            }), 400
        
        # Prepare data
        ratings_data, movies_data = prepare_recommendation_data()
        rec_engine.build_user_item_matrix(ratings_data)
        rec_engine.matrix_factorization(n_factors=10)
        
        # Evaluate different methods
        evaluation_results = {}
        
        # Evaluate collaborative filtering (user-user)
        uu_metrics = rec_engine.evaluate_recommendations(
            test_ratings,
            rec_engine.collaborative_filtering_user_user,
            n_recommendations=5
        )
        evaluation_results['user_user'] = uu_metrics
        
        # Evaluate matrix factorization
        mf_metrics = rec_engine.evaluate_recommendations(
            test_ratings,
            rec_engine.recommend_using_mf,
            n_recommendations=5
        )
        evaluation_results['matrix_factorization'] = mf_metrics
        
        return jsonify({
            'evaluation': evaluation_results,
            'total_ratings': len(test_ratings)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
