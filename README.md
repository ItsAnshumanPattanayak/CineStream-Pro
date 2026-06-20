# CineStream Pro - Movie Recommendation & Booking System

A comprehensive full-stack application combining **Netflix-like streaming experience** with **BookMyShow-like movie ticket booking**. Built with advanced machine learning algorithms for personalized movie recommendations.

## 🎯 Key Features

### 🎬 Movie Recommendations
- **Collaborative Filtering** (User-User & Item-Item)
- **Content-Based Filtering** (Genre/Tags)
- **Matrix Factorization** (NMF)
- **Hybrid Recommendations** combining all methods
- **Cosine Similarity** calculations for accurate matching
- **Personalized Recommendations** based on user interests
- **Trending & Popular Movies** algorithms

### 🎫 Movie Booking System
- **Real-time Seat Selection** with visual layout
- **Multiple Booking Types**:
  - In-theater bookings
  - Pre-bookings for future shows
  - Online streaming access
- **Theater & Show Management**
- **Seat Availability Tracking**
- **Show Schedules** by location and date

### 💳 Payment System
- **Dummy Payment Gateway** (for development)
- **Multiple Payment Methods**:
  - Credit Card
  - Debit Card
  - Digital Wallet
  - UPI
- **Payment Validation**
- **Transaction History**
- **Refund Processing**

### 👥 User Features
- **User Authentication** (JWT-based)
- **User Profiles** with interest preferences
- **Rating & Review System**
- **Booking History**
- **Watch List**
- **Payment History**

### 🎨 Frontend Features
- **Netflix-style UI** with dark theme
- **Responsive Design** (Mobile, Tablet, Desktop)
- **Real-time Search**
- **Movie Filtering & Sorting**
- **Interactive Movie Details**
- **Smooth Animations**

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLite (SQLAlchemy ORM)
- **ML Libraries**: scikit-learn, pandas, numpy
- **Authentication**: JWT
- **API**: RESTful with CORS support

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Styling**: CSS3 with Custom Properties
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: React Icons

## 📋 Project Structure

```
CineStream Pro/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── routes/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── movies.py         # Movie management
│   │   ├── recommendations.py # Recommendation engine
│   │   ├── bookings.py       # Booking management
│   │   ├── payments.py       # Payment processing
│   │   └── reviews.py        # Review system
│   ├── models/
│   │   └── database_models.py # SQLAlchemy models
│   ├── config/
│   └── utils/
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── components/       # React components
│       ├── pages/           # Page components
│       ├── services/        # API & state management
│       └── styles/          # Stylesheets
├── ml_models/
│   └── recommendation_engine.py # ML algorithms
├── data/                     # Dataset directory
├── database/                 # Database backups
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- Git

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd "e:\CineStream Pro\backend"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (already created, but update if needed):
   ```bash
   cat > .env << EOF
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///cinestream.db
   DEBUG=True
   EOF
   ```

5. **Initialize database**:
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

6. **Run backend server**:
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd "e:\CineStream Pro\frontend"
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create .env file**:
   ```bash
   echo REACT_APP_API_URL=http://localhost:5000/api > .env
   ```

4. **Start development server**:
   ```bash
   npm start
   ```
   Frontend will run on `http://localhost:3000`

## 📊 Machine Learning Models

### Collaborative Filtering
- **User-User**: Finds similar users and recommends movies they liked
- **Item-Item**: Finds similar movies based on user preferences
- Algorithm: Cosine Similarity

### Content-Based Filtering
- Uses genres and tags to find similar movies
- Algorithm: TF-IDF vectorization + Cosine Similarity

### Matrix Factorization
- Decomposes user-item matrix into latent factors
- Algorithm: Non-Negative Matrix Factorization (NMF)

### Hybrid Approach
- Combines all methods with weighted scoring
- Weights: User-User (30%), Item-Item (30%), Content (20%), MF (20%)

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile
- `POST /api/auth/change-password` - Change password

### Movies
- `GET /api/movies` - Get all movies
- `GET /api/movies/:id` - Get movie details
- `POST /api/movies/:id/rating` - Rate a movie
- `GET /api/movies/streaming` - Get streaming movies
- `GET /api/movies/trending` - Get trending movies

### Recommendations
- `GET /api/recommendations/personalized` - Get personalized recommendations
- `GET /api/recommendations/by-interest` - Recommendations by interest
- `GET /api/recommendations/similar-to/:id` - Similar movies
- `GET /api/recommendations/trending` - Trending recommendations

### Bookings
- `POST /api/bookings/create` - Create booking
- `GET /api/bookings/:id` - Get booking details
- `GET /api/bookings/:id/seats` - Get available seats
- `POST /api/bookings/pre-book` - Pre-book movie

### Payments
- `POST /api/payments/process` - Process payment
- `GET /api/payments/user/history` - Payment history
- `POST /api/payments/validate-card` - Validate card

### Reviews
- `POST /api/reviews/create` - Create review
- `GET /api/reviews/:id` - Get reviews

## 💾 Sample Data

Sample MovieLens-like data can be loaded using the data files in `data/` directory:
- `movies.csv` - Movie information
- `ratings.csv` - User ratings
- `shows.csv` - Theater shows

## 🧪 Testing

### Backend Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

### Frontend Testing
```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 🔒 Security

- JWT authentication for secure API access
- Password hashing with Werkzeug
- CORS protection
- Input validation on all endpoints
- Environment variables for sensitive data

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Pagination for large datasets
- Caching for recommendations
- Lazy loading in frontend
- Code splitting in React

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE.md for details

## 👨‍💻 Author

Built with ❤️ by the CineStream Pro Team

## 📧 Support

For support, email support@cinestreampro.com or open an issue in the repository

## 🙏 Acknowledgments

- MovieLens Dataset for recommendation system testing
- scikit-learn for ML algorithms
- Flask community for excellent documentation
- React community for amazing tools

---

**Happy coding! 🎬🎉**
