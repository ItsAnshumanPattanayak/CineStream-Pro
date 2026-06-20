import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../services/authStore';
import { toast } from 'react-toastify';
import './Navbar.css';

function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container container-lg">
        <Link to="/" className="navbar-brand">
          <span>🎬</span>
          <span>CineStream Pro</span>
        </Link>

        <div className="navbar-nav">
          <Link to="/">Home</Link>
          <Link to="/recommendations">Recommendations</Link>
          <Link to="/search">Browse</Link>
          {isAuthenticated && <Link to="/my-bookings">My Bookings</Link>}
        </div>

        <div className="navbar-actions">
          <form onSubmit={handleSearch} className="navbar-search">
            <input
              type="text"
              placeholder="Search movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>

          {isAuthenticated ? (
            <div className="navbar-user">
              <button className="btn btn-secondary">{user?.username}</button>
              <div className="user-menu" style={{ display: menuOpen ? 'block' : 'none' }}>
                <Link to="/profile">Profile</Link>
                <Link to="/my-bookings">My Bookings</Link>
                <button onClick={handleLogout}>Logout</button>
              </div>
            </div>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary">
                Login
              </Link>
              <Link to="/register" className="btn btn-primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
