import React from 'react';
import { FaFacebook, FaTwitter, FaInstagram, FaYoutube } from 'react-icons/fa';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>🎬 CineStream Pro</h3>
            <p>Your ultimate destination for movie recommendations and ticket booking.</p>
            <div className="social-links">
              <a href="#facebook" aria-label="Facebook">
                <FaFacebook />
              </a>
              <a href="#twitter" aria-label="Twitter">
                <FaTwitter />
              </a>
              <a href="#instagram" aria-label="Instagram">
                <FaInstagram />
              </a>
              <a href="#youtube" aria-label="YouTube">
                <FaYoutube />
              </a>
            </div>
          </div>

          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/recommendations">Recommendations</a></li>
              <li><a href="/search">Browse Movies</a></li>
              <li><a href="/my-bookings">My Bookings</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Features</h3>
            <ul>
              <li><a href="#movies">Streaming Movies</a></li>
              <li><a href="#bookings">Movie Bookings</a></li>
              <li><a href="#recommendations">Smart Recommendations</a></li>
              <li><a href="#reviews">Reviews & Ratings</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Support</h3>
            <ul>
              <li><a href="#help">Help Center</a></li>
              <li><a href="#faq">FAQ</a></li>
              <li><a href="#contact">Contact Us</a></li>
              <li><a href="#privacy">Privacy Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {currentYear} CineStream Pro. All rights reserved. | Built with ❤️ for movie lovers</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
