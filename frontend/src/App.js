import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import MovieDetails from './pages/MovieDetails';
import {
  SearchMovies,
  BookingPage,
  SeatSelection,
  PaymentPage,
  MyBookings,
  WatchMovie,
  Profile,
  Recommendations
} from './pages/index';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Services & Store
import { useAuthStore } from './services/authStore';
import './styles/App.css';

function App() {
  const { isAuthenticated, loadUser } = useAuthStore();

  useEffect(() => {
    // Load user from localStorage on app init
    loadUser();
  }, [loadUser]);

  return (
    <Router>
      <div className="app">
        <Navbar />
        
        <main className="app-main">
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
            <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/" />} />
            
            {/* Home & Exploration */}
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<SearchMovies />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/movie/:movieId" element={<MovieDetails />} />
            
            {/* Booking Routes */}
            <Route path="/booking/:showId" element={isAuthenticated ? <BookingPage /> : <Navigate to="/login" />} />
            <Route path="/booking/:bookingId/seats" element={isAuthenticated ? <SeatSelection /> : <Navigate to="/login" />} />
            <Route path="/payment/:bookingId" element={isAuthenticated ? <PaymentPage /> : <Navigate to="/login" />} />
            <Route path="/my-bookings" element={isAuthenticated ? <MyBookings /> : <Navigate to="/login" />} />
            
            {/* Streaming */}
            <Route path="/watch/:movieId" element={isAuthenticated ? <WatchMovie /> : <Navigate to="/login" />} />
            
            {/* User Profile */}
            <Route path="/profile" element={isAuthenticated ? <Profile /> : <Navigate to="/login" />} />
            
            {/* 404 */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>

        <Footer />
        <ToastContainer
          position="bottom-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  );
}

export default App;
