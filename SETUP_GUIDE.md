# CineStream Pro - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Overview](#project-overview)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Node.js 14+** and **npm** - Download from [nodejs.org](https://nodejs.org/)
- **Git** - Download from [git-scm.com](https://git-scm.com/)
- **Code Editor** - VS Code recommended from [code.visualstudio.com](https://code.visualstudio.com/)

### Verify Installations
```bash
# Check Python
python --version

# Check Node.js and npm
node --version
npm --version

# Check Git
git --version
```

---

## Project Overview

### Architecture
```
Frontend (React) <---> Backend API (Flask) <---> Database (SQLite)
                              |
                              v
                       ML Engine (scikit-learn)
```

### Key Features
- **Recommendation Engine**: ML-powered movie suggestions
- **Movie Booking**: In-theater ticket booking system
- **Online Streaming**: Watch movies online
- **User Ratings & Reviews**: Community ratings
- **Payment Processing**: Dummy payment gateway

---

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd "e:\CineStream Pro\backend"
```

### Step 2: Create Python Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask & CORS
- SQLAlchemy (ORM)
- scikit-learn & pandas (ML)
- JWT for authentication
- And other dependencies

### Step 4: Verify Installation
```bash
python -c "import flask, pandas, sklearn; print('All packages installed successfully!')"
```

### Step 5: Create Database
```bash
python
```

Then in Python shell:
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created successfully!")
exit()
```

### Step 6: Run Backend Server
```bash
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

✅ **Backend is running on `http://localhost:5000`**

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory
```bash
cd "e:\CineStream Pro\frontend"
```

### Step 2: Install Dependencies
```bash
npm install
```

This installs all React dependencies and may take 2-5 minutes.

### Step 3: Create Environment File
```bash
# On Windows (Command Prompt)
echo REACT_APP_API_URL=http://localhost:5000/api > .env

# On Windows (PowerShell)
"REACT_APP_API_URL=http://localhost:5000/api" | Out-File -Encoding UTF8 .env

# On macOS/Linux
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
```

### Step 4: Start Development Server
```bash
npm start
```

Expected output:
```
On Your Network: http://192.168.x.x:3000
Local:          http://localhost:3000
```

✅ **Frontend is running on `http://localhost:3000`**

---

## Database Setup

### Create Sample Data

Navigate to backend and create a Python script to add sample data:

```python
from app import app, db
from models.database_models import Movie, User, Rating, Theater, Theater_Show
from datetime import datetime, timedelta

with app.app_context():
    # Create sample movies
    movie1 = Movie(
        title="The Action Hero",
        description="A thrilling action movie",
        genre=["Action", "Adventure"],
        tags=["Hollywood", "2023"],
        director="John Doe",
        cast=["Actor A", "Actor B"],
        release_date=datetime(2023, 6, 1),
        duration_minutes=120,
        rating=4.5,
        streaming_available=True,
        language="English"
    )
    
    movie2 = Movie(
        title="Comedy Night",
        description="A hilarious comedy film",
        genre=["Comedy"],
        tags=["Hollywood", "2023"],
        director="Jane Smith",
        cast=["Actor C", "Actor D"],
        release_date=datetime(2023, 7, 1),
        duration_minutes=110,
        rating=4.2,
        streaming_available=True,
        language="English"
    )
    
    db.session.add(movie1)
    db.session.add(movie2)
    db.session.commit()
    
    print("Sample movies added!")
```

---

## Running the Application

### Recommended Setup: Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd "e:\CineStream Pro\backend"
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd "e:\CineStream Pro\frontend"
npm start
```

### Using the Auto-Setup Script (Windows only)
```bash
cd "e:\CineStream Pro"
setup.bat
```

---

## Testing

### Test Backend API

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Register User:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "interests": ["Action", "Comedy"]
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Test Frontend

1. Open `http://localhost:3000` in your browser
2. Click "Sign Up" and create an account
3. Select your favorite genres
4. Click "Home" to see recommendations
5. Browse movies and ratings

### Run Automated Tests

**Backend Tests:**
```bash
cd backend
pytest tests/
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'flask'"**
- Solution: Make sure virtual environment is activated
  ```bash
  venv\Scripts\activate  # Windows
  source venv/bin/activate  # macOS/Linux
  ```

**Error: "Port 5000 is already in use"**
- Solution 1: Kill the process using port 5000
  ```bash
  # Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  
  # macOS/Linux
  lsof -ti:5000 | xargs kill -9
  ```
- Solution 2: Use a different port
  ```bash
  python app.py --port 5001
  ```

**Error: "Database file not found"**
- Solution: Reinitialize the database
  ```bash
  rm cinestream.db  # Delete old database
  python
  >>> from app import app, db
  >>> with app.app_context():
  ...     db.create_all()
  ```

### Frontend Issues

**Error: "npm ERR! EACCES: permission denied"**
- Solution: Clear npm cache and reinstall
  ```bash
  npm cache clean --force
  rm -rf node_modules package-lock.json
  npm install
  ```

**Error: "Cannot find module 'react'"**
- Solution: Reinstall dependencies
  ```bash
  cd frontend
  npm install
  ```

**Error: "Blank white screen or 404 errors"**
- Solution 1: Check if backend is running
  ```bash
  curl http://localhost:5000/api/health
  ```
- Solution 2: Clear browser cache
  - Press `Ctrl + Shift + Delete` in browser
  - Clear "All time" data
  - Reload page

**CORS Error: "Access to XMLHttpRequest blocked"**
- Solution: Ensure backend is running on port 5000
- Check that `.env` has correct API URL:
  ```
  REACT_APP_API_URL=http://localhost:5000/api
  ```

### Common Issues

**Issue: Changes not reflecting**
- Frontend: Hard refresh with `Ctrl + Shift + R` or `Cmd + Shift + R`
- Backend: Server restarts automatically in debug mode, otherwise run again

**Issue: 401 Unauthorized errors**
- Solution: Log out and log back in
- Clear localStorage: `localStorage.clear()` in browser console

**Issue: Database locked error**
- Solution: Restart the backend server
- Close any other connections to the database

---

## Development Tools

### Recommended VS Code Extensions
- Python (Microsoft)
- Pylance
- ES7+ React/Redux/React-Native snippets
- Thunder Client (or Postman)
- SQLite Viewer

### Useful Commands

**Backend**
```bash
# Run with specific environment
FLASK_ENV=production python app.py

# Run tests with coverage
pytest --cov=.

# Format code
black .

# Lint code
pylint routes/ models/
```

**Frontend**
```bash
# Build for production
npm run build

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Eject configuration (irreversible!)
npm run eject
```

---

## Next Steps

1. **Populate Sample Data**: Add movies, ratings, and shows to the database
2. **Build ML Models**: Train recommendation models with MovieLens dataset
3. **Complete Frontend Pages**: Implement MovieDetails, Search, Booking pages
4. **Add Features**:
   - User watchlist
   - Social features (follow users)
   - Advanced filtering
   - Real payment integration
5. **Deploy**: Use platforms like Heroku, AWS, or DigitalOcean

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [REST API Best Practices](https://restfulapi.net/)

---

## Support

- Check existing issues on GitHub
- Review error messages carefully
- Check backend logs for API errors
- Check browser console for frontend errors
- Post questions on Stack Overflow

---

**Happy Coding! 🎬🚀**
