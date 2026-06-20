from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import extensions
from extensions import db, login_manager

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cinestream.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MOVIELENS_PATH'] = os.getenv('MOVIELENS_PATH', 'data/ml-latest-small/')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Import and register blueprints (import here to avoid circular imports)
    with app.app_context():
        from routes.auth import auth_bp
        from routes.movies import movies_bp
        from routes.recommendations import recommendations_bp
        from routes.bookings import bookings_bp
        from routes.payments import payments_bp
        from routes.reviews import reviews_bp

        # Register blueprints
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(movies_bp, url_prefix='/api/movies')
        app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
        app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
        app.register_blueprint(payments_bp, url_prefix='/api/payments')
        app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

        # Create database tables
        db.create_all()

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'CineStream Pro API is running'}, 200

    @app.route('/')
    def index():
        """Serve frontend"""
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files"""
        return send_from_directory(app.static_folder, path)

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Initialize data and recommendation engine
    with app.app_context():
        from utils.data_loader import initialize_database
        from utils.recommendation_trainer import train_recommendation_model
        
        # Load initial data if database is empty
        initialize_database()
        
        # Train recommendation model
        train_recommendation_model()
    
    app.run(debug=True, host='0.0.0.0', port=5000)