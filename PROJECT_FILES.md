# CineStream Pro - Project Files Reference

## 📁 Project Structure Overview

```
CineStream Pro/
├── 📄 README.md                    # Project overview & features
├── 📄 SETUP_GUIDE.md              # Detailed setup & troubleshooting
├── 📄 QUICK_START.md              # 5-minute quick start
├── 📄 PROJECT_FILES.md            # This file
├── 📄 setup.bat                   # Windows auto-setup script
│
├── 📁 backend/                    # Python Flask Backend
│   ├── 📄 app.py                  # Flask main application
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 .env                    # Environment variables
│   │
│   ├── 📁 routes/                 # API Routes
│   │   ├── __init__.py
│   │   ├── auth.py                # Auth endpoints (register, login)
│   │   ├── movies.py              # Movie endpoints (CRUD, search)
│   │   ├── recommendations.py     # Recommendation endpoints
│   │   ├── bookings.py            # Booking endpoints
│   │   ├── payments.py            # Payment endpoints
│   │   └── reviews.py             # Review endpoints
│   │
│   ├── 📁 models/                 # Database Models
│   │   ├── __init__.py
│   │   └── database_models.py     # SQLAlchemy ORM models
│   │
│   └── 📁 config/                 # Configuration (empty)
│
├── 📁 frontend/                   # React Frontend
│   ├── 📄 package.json            # npm dependencies
│   ├── 📄 .env                    # Frontend environment variables
│   │
│   ├── 📁 public/
│   │   └── index.html             # HTML entry point
│   │
│   └── 📁 src/                    # React Source Code
│       ├── 📄 index.js            # React entry point
│       ├── 📄 App.js              # Main App component with routing
│       │
│       ├── 📁 components/         # Reusable Components
│       │   ├── Navbar.js          # Navigation bar
│       │   ├── Navbar.css
│       │   ├── Footer.js          # Footer
│       │   └── Footer.css
│       │
│       ├── 📁 pages/              # Page Components
│       │   ├── index.js           # Placeholder pages
│       │   ├── Home.js            # Home page
│       │   ├── Home.css
│       │   ├── Login.js           # Login page
│       │   ├── Register.js        # Registration page
│       │   ├── Auth.css           # Auth pages styling
│       │   ├── MovieDetails.js    # Movie details (placeholder)
│       │   ├── SearchMovies.js    # Search (placeholder)
│       │   ├── BookingPage.js     # Booking (placeholder)
│       │   ├── SeatSelection.js   # Seats (placeholder)
│       │   ├── PaymentPage.js     # Payment (placeholder)
│       │   ├── MyBookings.js      # Bookings (placeholder)
│       │   ├── WatchMovie.js      # Streaming (placeholder)
│       │   ├── Profile.js         # Profile (placeholder)
│       │   └── Recommendations.js # Recommendations (placeholder)
│       │
│       ├── 📁 services/           # API & State Management
│       │   ├── api.js             # API client with all endpoints
│       │   └── authStore.js       # Zustand auth store
│       │
│       └── 📁 styles/             # Global Styles
│           ├── index.css          # Global styles
│           └── App.css            # App component styles
│
├── 📁 ml_models/                  # Machine Learning
│   ├── __init__.py
│   └── recommendation_engine.py  # ML algorithms & recommendation logic
│
├── 📁 data/                       # Dataset Directory (empty)
│   └── [MovieLens data goes here]
│
└── 📁 database/                   # Database Backups (empty)
    └── [Database backups go here]
```

---

## 📄 File Descriptions

### Root Files
- **README.md** - Complete project overview, features, tech stack, and API documentation
- **SETUP_GUIDE.md** - Detailed setup instructions with troubleshooting guide
- **QUICK_START.md** - 5-minute quick start guide
- **setup.bat** - Windows batch script to automate setup
- **PROJECT_FILES.md** - This file describing all files

### Backend - Core Application
- **app.py** - Flask application initialization, configuration, route registration, and database setup

### Backend - Routes (API Endpoints)
- **routes/auth.py** - User authentication (register, login, logout, profile management)
- **routes/movies.py** - Movie management (list, search, filter, ratings)
- **routes/recommendations.py** - ML-powered recommendations (5 different algorithms)
- **routes/bookings.py** - Theater booking (create, cancel, seat selection)
- **routes/payments.py** - Payment processing (dummy gateway, validation, refunds)
- **routes/reviews.py** - Movie reviews and ratings

### Backend - Data Models
- **models/database_models.py** - SQLAlchemy ORM models for:
  - User (authentication, preferences)
  - Movie (details, metadata)
  - Rating (user ratings)
  - Review (user reviews)
  - Theater (venue information)
  - Theater_Show (show details)
  - Seat (theater seats)
  - Booking (ticket bookings)
  - Payment (payment records)

### Backend - ML Module
- **ml_models/recommendation_engine.py** - Comprehensive recommendation engine with:
  - Collaborative Filtering (User-User, Item-Item)
  - Content-Based Filtering
  - Matrix Factorization (NMF)
  - Hybrid Approach
  - Cosine Similarity calculations
  - Evaluation metrics

### Backend - Configuration
- **requirements.txt** - All Python dependencies
- **.env** - Environment variables (SECRET_KEY, DATABASE_URL, etc.)

### Frontend - Core
- **index.js** - React DOM entry point
- **App.js** - Main application component with routing setup
- **.env** - Frontend environment variables (API URL)

### Frontend - Components
- **components/Navbar.js** - Navigation bar with search and user menu
- **components/Footer.js** - Footer with links and social media

### Frontend - Pages
- **pages/Home.js** - Home page with recommendations and trending movies
- **pages/Login.js** - Login form with validation
- **pages/Register.js** - Registration with genre selection
- **pages/MovieDetails.js** - Movie details (placeholder)
- **pages/SearchMovies.js** - Movie search (placeholder)
- **pages/BookingPage.js** - Theater booking (placeholder)
- **pages/SeatSelection.js** - Seat selection (placeholder)
- **pages/PaymentPage.js** - Payment processing (placeholder)
- **pages/MyBookings.js** - User bookings (placeholder)
- **pages/WatchMovie.js** - Online streaming (placeholder)
- **pages/Profile.js** - User profile (placeholder)
- **pages/Recommendations.js** - Recommendations page (placeholder)

### Frontend - Services
- **services/api.js** - Axios API client with all endpoint functions
- **services/authStore.js** - Zustand auth state management

### Frontend - Styles
- **styles/index.css** - Global CSS variables, typography, and utilities
- **styles/App.css** - Main app layout and component styles
- **components/Navbar.css** - Navbar specific styles
- **components/Footer.css** - Footer specific styles
- **pages/Home.css** - Home page styles
- **pages/Auth.css** - Login/Register page styles

---

## 🔑 Key Files to Modify First

### For Adding Features
1. **backend/routes/** - Add new endpoints
2. **backend/models/database_models.py** - Modify database schema
3. **frontend/src/pages/** - Complete placeholder page implementations
4. **frontend/src/services/api.js** - Add new API calls

### For Customization
1. **frontend/src/styles/index.css** - Change colors and theme
2. **README.md** - Update project description
3. **backend/.env** - Configure environment

### For ML Improvements
1. **ml_models/recommendation_engine.py** - Enhance algorithms
2. **backend/routes/recommendations.py** - Add new recommendation types

---

## 📊 File Statistics

| Category | Count | Total Lines |
|----------|-------|-------------|
| Backend Routes | 6 | ~1,500 |
| Database Models | 1 | ~500 |
| ML Engine | 1 | ~600 |
| Frontend Pages | 10 | ~1,200 |
| Frontend Components | 2 | ~300 |
| Styles | 5 | ~600 |
| Config & Docs | 5 | ~1,000 |
| **Total** | **30** | **~6,000** |

---

## 🚀 How to Use These Files

### Getting Started
1. Read **QUICK_START.md** (5 minutes)
2. Follow **SETUP_GUIDE.md** if needed
3. Run the application

### Development
1. Backend changes: Modify files in `backend/routes/` or `backend/models/`
2. Frontend changes: Modify files in `frontend/src/`
3. Style changes: Update `frontend/src/styles/` and component CSS files

### Feature Addition
1. Add backend endpoint in appropriate `routes/` file
2. Add API function in `frontend/src/services/api.js`
3. Create/Update page in `frontend/src/pages/`
4. Add styles as needed

### Deployment
1. Build frontend: `npm run build`
2. Serve with backend or static hosting
3. Update `.env` for production URLs
4. Switch database to PostgreSQL

---

## 📋 Checklist for First Run

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Both backends activated in separate terminals
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access home page
- [ ] Can create account
- [ ] Can view recommendations

---

## 🔗 File Relationships

```
app.py (Main)
  ├── routes/auth.py → models/database_models.py (User)
  ├── routes/movies.py → models/database_models.py (Movie)
  ├── routes/recommendations.py → ml_models/recommendation_engine.py
  ├── routes/bookings.py → models/database_models.py (Booking)
  ├── routes/payments.py → models/database_models.py (Payment)
  └── routes/reviews.py → models/database_models.py (Review)

App.js (Frontend)
  ├── pages/*.js → services/api.js
  ├── services/api.js → Backend endpoints
  ├── services/authStore.js → Zustand state
  └── components/ → pages/
```

---

## 📝 Notes

- All placeholder pages are functional but need full implementation
- Database defaults to SQLite - change in `.env` for PostgreSQL
- Payment gateway is dummy - integrate real gateway for production
- Images use URLs - implement file uploads for production
- ML models need MovieLens data to train - included in `data/` directory

---

**For questions, refer to the documentation files or code comments! 🎬**
