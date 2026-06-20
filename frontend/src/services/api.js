import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth APIs
export const authAPI = {
  register: (userData) => apiClient.post('/auth/register', userData),
  login: (credentials) => apiClient.post('/auth/login', credentials),
  logout: () => apiClient.post('/auth/logout'),
  getProfile: () => apiClient.get('/auth/profile'),
  updateProfile: (data) => apiClient.put('/auth/profile', data),
  changePassword: (data) => apiClient.post('/auth/change-password', data)
};

// Movies APIs
export const moviesAPI = {
  getAllMovies: (page = 1, perPage = 10, filters = {}) => 
    apiClient.get('/movies', { params: { page, per_page: perPage, ...filters } }),
  getMovieById: (movieId) => apiClient.get(`/movies/${movieId}`),
  getMovieShows: (movieId) => apiClient.get(`/movies/${movieId}/shows`),
  rateMovie: (movieId, rating) => apiClient.post(`/movies/${movieId}/rating`, { rating }),
  getMovieRatings: (movieId) => apiClient.get(`/movies/${movieId}/ratings`),
  getStreamingMovies: (page = 1, perPage = 10) =>
    apiClient.get('/movies/streaming', { params: { page, per_page: perPage } }),
  getTrendingMovies: () => apiClient.get('/movies/trending')
};

// Recommendations APIs
export const recommendationsAPI = {
  getPersonalized: (n = 5, method = 'hybrid') =>
    apiClient.get('/recommendations/personalized', { params: { n, method } }),
  getByInterest: (n = 5) =>
    apiClient.get('/recommendations/by-interest', { params: { n } }),
  getSimilarMovies: (movieId, n = 5) =>
    apiClient.get(`/recommendations/similar-to/${movieId}`, { params: { n } }),
  getTrending: (n = 10) =>
    apiClient.get('/recommendations/trending', { params: { n } }),
  getPopular: (n = 10) =>
    apiClient.get('/recommendations/popular', { params: { n } }),
  getWatchedBased: (n = 5) =>
    apiClient.get('/recommendations/watched', { params: { n } })
};

// Bookings APIs
export const bookingsAPI = {
  createBooking: (data) => apiClient.post('/bookings/create', data),
  cancelBooking: (bookingId) => apiClient.post(`/bookings/cancel/${bookingId}`),
  getBooking: (bookingId) => apiClient.get(`/bookings/${bookingId}`),
  getUserBookings: (filters = {}) =>
    apiClient.get('/bookings/user/all', { params: filters }),
  getShowSeats: (showId) => apiClient.get(`/bookings/${showId}/seats`),
  preBookMovie: (data) => apiClient.post('/bookings/pre-book', data),
  upgradeToBooked: (bookingId, seatIds) =>
    apiClient.post(`/bookings/${bookingId}/upgrade-to-paid`, { seat_ids: seatIds })
};

// Payments APIs
export const paymentsAPI = {
  processPayment: (data) => apiClient.post('/payments/process', data),
  getPayment: (paymentId) => apiClient.get(`/payments/${paymentId}`),
  getBookingPayment: (bookingId) => apiClient.get(`/payments/booking/${bookingId}`),
  validateCard: (cardData) => apiClient.post('/payments/validate-card', cardData),
  refundPayment: (paymentId) => apiClient.post(`/payments/refund/${paymentId}`),
  getPaymentHistory: () => apiClient.get('/payments/user/history'),
  getPaymentStats: () => apiClient.get('/payments/stats')
};

// Reviews APIs
export const reviewsAPI = {
  createReview: (data) => apiClient.post('/reviews/create', data),
  getMovieReviews: (movieId, page = 1, perPage = 10, sortBy = 'recent') =>
    apiClient.get(`/reviews/${movieId}`, { params: { page, per_page: perPage, sort_by: sortBy } }),
  getReview: (reviewId) => apiClient.get(`/reviews/${reviewId}`),
  updateReview: (reviewId, data) => apiClient.put(`/reviews/${reviewId}`, data),
  deleteReview: (reviewId) => apiClient.delete(`/reviews/${reviewId}`),
  getUserReviews: () => apiClient.get('/reviews/user/all'),
  getReviewStats: (movieId) => apiClient.get(`/reviews/stats/${movieId}`)
};

export default apiClient;
