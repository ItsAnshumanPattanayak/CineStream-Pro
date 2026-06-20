import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { moviesAPI, recommendationsAPI } from '../services/api';
import { useAuthStore } from '../services/authStore';
import './Home.css';

function Home() {
  const { isAuthenticated, user } = useAuthStore();
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [streamingMovies, setStreamingMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      setLoading(true);
      
      if (isAuthenticated) {
        const recRes = await recommendationsAPI.getPersonalized(5);
        setRecommendedMovies(recRes.data.recommendations || []);
      }

      const trendRes = await recommendationsAPI.getTrending(6);
      setTrendingMovies(trendRes.data.trending_movies || []);

      const streamRes = await moviesAPI.getStreamingMovies(1, 6);
      setStreamingMovies(streamRes.data.movies || []);
    } catch (error) {
      console.error('Error fetching home data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to CineStream Pro</h1>
          <p>Stream movies online or book tickets at your favorite theaters</p>
          {!isAuthenticated && (
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg">
                Get Started
              </Link>
              <Link to="/search" className="btn btn-outline btn-lg">
                Browse Movies
              </Link>
            </div>
          )}
          {isAuthenticated && (
            <div className="hero-actions">
              <Link to="/recommendations" className="btn btn-primary btn-lg">
                Discover For You
              </Link>
              <Link to="/search" className="btn btn-outline btn-lg">
                Browse All Movies
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Personalized Recommendations */}
      {isAuthenticated && recommendedMovies.length > 0 && (
        <section className="home-section">
          <div className="section-header">
            <h2>Recommended For {user?.first_name || user?.username}</h2>
            <Link to="/recommendations">See all</Link>
          </div>
          <div className="movies-grid grid-4">
            {recommendedMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        </section>
      )}

      {/* Trending Movies */}
      {trendingMovies.length > 0 && (
        <section className="home-section">
          <div className="section-header">
            <h2>Trending Now</h2>
            <Link to="/search?sort=trending">See all</Link>
          </div>
          <div className="movies-grid grid-4">
            {trendingMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        </section>
      )}

      {/* Streaming Movies */}
      {streamingMovies.length > 0 && (
        <section className="home-section">
          <div className="section-header">
            <h2>Stream Now</h2>
            <Link to="/search?streaming=true">See all</Link>
          </div>
          <div className="movies-grid grid-4">
            {streamingMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} isStreamable={true} />
            ))}
          </div>
        </section>
      )}

      {loading && !recommendedMovies.length && (
        <div className="loading-container">
          <div className="loading"></div>
        </div>
      )}
    </div>
  );
}

function MovieCard({ movie, isStreamable }) {
  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="movie-poster">
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} />
        ) : (
          <div className="poster-placeholder">No Image</div>
        )}
        {isStreamable && <div className="stream-badge">Stream Now</div>}
      </div>
      <div className="movie-info">
        <h3>{movie.title}</h3>
        <div className="movie-meta">
          <span className="rating">⭐ {movie.rating?.toFixed(1) || 'N/A'}</span>
          <span className="year">{movie.release_date?.split('-')[0]}</span>
        </div>
        <div className="movie-genres">
          {movie.genre?.slice(0, 2).map((g) => (
            <span key={g} className="genre-tag">{g}</span>
          ))}
        </div>
      </div>
    </Link>
  );
}

export default Home;
