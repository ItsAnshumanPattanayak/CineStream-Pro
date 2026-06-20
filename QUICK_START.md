# CineStream Pro - Quick Start Guide (5 Minutes)

## 🚀 Getting Started in 5 Minutes

### Prerequisites Check (1 minute)
```bash
python --version        # Should be 3.8+
node --version         # Should be 14+
npm --version          # Should be 6+
```

### Backend Startup (2 minutes)

**Terminal 1:**
```bash
cd "e:\CineStream Pro\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

✅ Backend ready on http://localhost:5000

### Frontend Startup (2 minutes)

**Terminal 2:**
```bash
cd "e:\CineStream Pro\frontend"
npm install
npm start
```

✅ Frontend ready on http://localhost:3000

---

## 🎯 First Things to Try

1. **Open Browser**: http://localhost:3000
2. **Sign Up**: Click "Sign Up" → Create account → Select genres
3. **Explore**: Click "Home" → See recommendations
4. **Browse**: Click "Browse Movies" → Search and filter

---

## 📊 What's Implemented

### ✅ Complete
- User registration and authentication
- Movie management and ratings
- Recommendation engine (5 algorithms)
- Booking system
- Payment processing
- Review system
- Theater and show management

### ⏳ In Development
- Full page implementations
- Video streaming
- Seat selection UI
- Advanced filtering

---

## 🔌 Test the API (Optional)

```bash
# Health check
curl http://localhost:5000/api/health

# Get all movies
curl http://localhost:5000/api/movies
```

---

## 📖 Full Documentation

- **Setup Details**: See `SETUP_GUIDE.md`
- **Features**: See `README.md`
- **Troubleshooting**: See `SETUP_GUIDE.md` → Troubleshooting

---

## 💡 Pro Tips

1. **Hot Reload**: Frontend reloads automatically on changes
2. **Debug Mode**: Backend runs in debug mode - restart for changes
3. **Database**: SQLite file is created automatically
4. **API Testing**: Use Postman or Thunder Client
5. **Clear Cache**: `Ctrl + Shift + Delete` in browser if issues

---

## ❓ Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Kill process or use different port |
| npm install fails | Delete node_modules & try again |
| Backend won't start | Check Python version, activate venv |
| Frontend blank screen | Check if backend running, clear cache |
| CORS errors | Ensure backend on port 5000 |

---

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` → Troubleshooting
2. Review error messages carefully
3. Check browser console (F12)
4. Check terminal output
5. Restart both servers

---

**Ready? Open http://localhost:3000 and start building! 🎬🎉**
