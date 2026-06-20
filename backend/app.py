from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cinestream.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
db = SQLAlchemy(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import blueprints
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'CineStream Pro API is running'}, 200

@app.route('/', methods=['GET'])
def index():
    """Welcome endpoint"""
    return {
        'app': 'CineStream Pro - Movie Recommendation & Booking System',
        'version': '1.0.0',
        'status': 'running'
    }, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
