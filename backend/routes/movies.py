from flask import Blueprint, request, jsonify
from extensions import db
from models.movie import Movie
from models.rating import Rating

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/', methods=['GET'])
def get_movies():
    """Get all movies with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    genre = request.args.get('genre')
    search = request.args.get('search')
    streaming = request.args.get('streaming', type=bool)
    in_theaters = request.args.get('in_theaters', type=bool)
    
    query = Movie.query
    
    if genre:
        query = query.filter(Movie.genres.contains(genre))
    
    if search:
        query = query.filter(Movie.title.contains(search))
    
    if streaming is not None:
        query = query.filter_by(is_streaming=streaming)
    
    if in_theaters is not None:
        query = query.filter_by(is_in_theaters=in_theaters)
    
    movies = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'movies': [m.to_dict() for m in movies.items],
        'total': movies.total,
        'pages': movies.pages,
        'current_page': movies.page
    })

@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get detailed movie information"""
    movie = Movie.query.get_or_404(movie_id)
    
    # Get average rating
    avg_rating = db.session.query(db.func.avg(Rating.rating)).filter_by(movie_id=movie_id).scalar()
    num_ratings = Rating.query.filter_by(movie_id=movie_id).count()
    
    # Get recent reviews
    reviews = Rating.query.filter_by(movie_id=movie_id)\
        .filter(Rating.review.isnot(None))\
        .order_by(Rating.timestamp.desc())\
        .limit(5).all()
    
    movie_dict = movie.to_dict()
    movie_dict['avg_rating'] = float(avg_rating) if avg_rating else None
    movie_dict['num_ratings'] = num_ratings
    movie_dict['reviews'] = [{
        'user': r.user.username,
        'rating': r.rating,
        'review': r.review,
        'timestamp': r.timestamp.isoformat()
    } for r in reviews]
    
    return jsonify(movie_dict)

@movies_bp.route('/genres', methods=['GET'])
def get_genres():
    """Get all available genres"""
    genres = db.session.query(Movie.genres).distinct().all()
    
    all_genres = set()
    for g in genres:
        if g[0]:
            all_genres.update(g[0].split('|'))
    
    return jsonify({'genres': sorted(list(all_genres))})