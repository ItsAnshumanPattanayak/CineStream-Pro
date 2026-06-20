from flask import Blueprint, request, jsonify
from app import db
from models.database_models import Movie, Rating, Theater_Show, Theater
from routes.auth import token_required
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

movies_bp = Blueprint('movies', __name__)


@movies_bp.route('/', methods=['GET'])
def get_all_movies():
    """Get all movies with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filters
        genre = request.args.get('genre')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'rating')  # rating, release_date, title
        
        query = Movie.query
        
        # Apply filters
        if genre:
            query = query.filter(Movie.genre.contains(genre))
        
        if search:
            query = query.filter(
                or_(
                    Movie.title.ilike(f'%{search}%'),
                    Movie.description.ilike(f'%{search}%')
                )
            )
        
        # Sort
        if sort_by == 'rating':
            query = query.order_by(Movie.rating.desc())
        elif sort_by == 'release_date':
            query = query.order_by(Movie.release_date.desc())
        elif sort_by == 'title':
            query = query.order_by(Movie.title.asc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'movies': [movie.to_dict() for movie in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get specific movie details"""
    try:
        movie = Movie.query.get(movie_id)
        
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        # Get average rating
        avg_rating = db.session.query(db.func.avg(Rating.rating)).filter(
            Rating.movie_id == movie_id
        ).scalar()
        
        movie.rating = float(avg_rating) if avg_rating else 0.0
        
        return jsonify({
            'movie': movie.to_dict(include_details=True),
            'average_rating': movie.rating,
            'total_ratings': Rating.query.filter_by(movie_id=movie_id).count()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/<int:movie_id>/shows', methods=['GET'])
def get_movie_shows(movie_id):
    """Get all shows for a movie"""
    try:
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        # Get shows from today onwards
        today = datetime.utcnow().date()
        shows = Theater_Show.query.filter(
            and_(
                Theater_Show.movie_id == movie_id,
                Theater_Show.show_date >= today
            )
        ).all()
        
        # Group by theater
        shows_by_theater = {}
        for show in shows:
            theater_id = show.theater_id
            if theater_id not in shows_by_theater:
                shows_by_theater[theater_id] = {
                    'theater': show.theater.to_dict(),
                    'shows': []
                }
            shows_by_theater[theater_id]['shows'].append(show.to_dict())
        
        return jsonify({
            'movie_id': movie_id,
            'movie_title': movie.title,
            'theaters': list(shows_by_theater.values())
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/<int:movie_id>/rating', methods=['POST'])
@token_required
def rate_movie(current_user, movie_id):
    """Rate a movie"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        
        if not rating or rating < 1 or rating > 5:
            return jsonify({'message': 'Rating must be between 1 and 5'}), 400
        
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
        
        # Check if user already rated this movie
        existing_rating = Rating.query.filter_by(
            user_id=current_user.id,
            movie_id=movie_id
        ).first()
        
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.timestamp = datetime.utcnow()
        else:
            new_rating = Rating(
                user_id=current_user.id,
                movie_id=movie_id,
                rating=rating
            )
            db.session.add(new_rating)
        
        db.session.commit()
        
        # Update movie average rating
        avg_rating = db.session.query(db.func.avg(Rating.rating)).filter(
            Rating.movie_id == movie_id
        ).scalar()
        movie.rating = float(avg_rating) if avg_rating else 0.0
        db.session.commit()
        
        return jsonify({
            'message': 'Rating saved successfully',
            'movie_rating': movie.rating
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/<int:movie_id>/ratings', methods=['GET'])
def get_movie_ratings(movie_id):
    """Get ratings statistics for a movie"""
    try:
        ratings = Rating.query.filter_by(movie_id=movie_id).all()
        
        if not ratings:
            return jsonify({
                'movie_id': movie_id,
                'total_ratings': 0,
                'average_rating': 0,
                'rating_distribution': {}
            }), 200
        
        # Calculate statistics
        ratings_list = [r.rating for r in ratings]
        
        # Rating distribution
        distribution = {}
        for i in range(1, 6):
            count = sum(1 for r in ratings_list if r == i)
            distribution[str(i)] = count
        
        return jsonify({
            'movie_id': movie_id,
            'total_ratings': len(ratings),
            'average_rating': sum(ratings_list) / len(ratings_list),
            'rating_distribution': distribution
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/streaming', methods=['GET'])
def get_streaming_movies():
    """Get movies available for streaming"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        movies = Movie.query.filter_by(
            streaming_available=True
        ).order_by(Movie.rating.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'movies': [movie.to_dict() for movie in movies.items],
            'total': movies.total,
            'pages': movies.pages
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@movies_bp.route('/trending', methods=['GET'])
def get_trending_movies():
    """Get trending movies based on recent ratings"""
    try:
        # Get movies with recent ratings
        recent_date = datetime.utcnow() - timedelta(days=7)
        
        trending = db.session.query(
            Movie,
            db.func.count(Rating.id).label('rating_count'),
            db.func.avg(Rating.rating).label('avg_rating')
        ).join(Rating).filter(
            Rating.timestamp >= recent_date
        ).group_by(Movie.id).order_by(
            db.func.count(Rating.id).desc()
        ).limit(10).all()
        
        result = []
        for movie, count, avg_rating in trending:
            movie_dict = movie.to_dict()
            movie_dict['recent_ratings'] = count
            movie_dict['rating'] = float(avg_rating) if avg_rating else 0
            result.append(movie_dict)
        
        return jsonify({
            'trending_movies': result
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
