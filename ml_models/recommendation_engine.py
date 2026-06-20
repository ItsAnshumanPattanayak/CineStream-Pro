import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from typing import List, Dict, Tuple
import json

class RecommendationEngine:
    """
    Movie Recommendation Engine using:
    - Collaborative Filtering (User-User & Item-Item)
    - Content-Based Filtering (Genre & Tags)
    - Matrix Factorization (NMF)
    """
    
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarity = None
        self.item_similarity = None
        self.nmf_model = None
        self.user_features = None
        self.movie_features = None
        self.tfidf_vectorizer = None
        self.content_features = None
    
    def build_user_item_matrix(self, ratings_data: List[Dict]) -> pd.DataFrame:
        """
        Build user-item rating matrix from ratings data
        
        Args:
            ratings_data: List of dicts with user_id, movie_id, rating
            
        Returns:
            User-Item rating matrix (DataFrame)
        """
        if not ratings_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(ratings_data)
        user_item_matrix = df.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating',
            fill_value=0
        )
        self.user_item_matrix = user_item_matrix
        return user_item_matrix
    
    def build_content_features(self, movies_data: List[Dict]) -> np.ndarray:
        """
        Build content-based features using genres and tags
        
        Args:
            movies_data: List of dicts with movie info (title, genres, tags)
            
        Returns:
            TF-IDF features for content-based filtering
        """
        if not movies_data:
            return np.array([])
        
        # Combine genres and tags for each movie
        content_strings = []
        for movie in movies_data:
            genres = ' '.join(movie.get('genre', []))
            tags = ' '.join(movie.get('tags', []))
            content_strings.append(f"{genres} {tags}".strip())
        
        # Apply TF-IDF vectorization
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100)
        self.content_features = self.tfidf_vectorizer.fit_transform(content_strings)
        
        return self.content_features
    
    def collaborative_filtering_user_user(self, user_id: int, n_recommendations: int = 5) -> List[int]:
        """
        User-User Collaborative Filtering
        Find similar users and recommend movies they liked
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of movies to recommend
            
        Returns:
            List of recommended movie IDs
        """
        if self.user_item_matrix is None or user_id not in self.user_item_matrix.index:
            return []
        
        # Calculate user similarity matrix using cosine similarity
        user_similarity = cosine_similarity(self.user_item_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
        
        # Get similar users (excluding self)
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:6]
        
        # Get movies rated by similar users that current user hasn't rated
        user_rated_movies = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
        recommendations = {}
        
        for sim_user, similarity_score in similar_users.items():
            sim_user_ratings = self.user_item_matrix.loc[sim_user]
            for movie_id, rating in sim_user_ratings.items():
                if movie_id not in user_rated_movies and rating > 0:
                    if movie_id not in recommendations:
                        recommendations[movie_id] = 0
                    recommendations[movie_id] += similarity_score * rating
        
        # Sort by score and return top N
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [movie_id for movie_id, _ in sorted_recs[:n_recommendations]]
    
    def collaborative_filtering_item_item(self, user_id: int, n_recommendations: int = 5) -> List[int]:
        """
        Item-Item Collaborative Filtering
        Find similar movies to ones user liked
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of movies to recommend
            
        Returns:
            List of recommended movie IDs
        """
        if self.user_item_matrix is None or user_id not in self.user_item_matrix.index:
            return []
        
        # Calculate item (movie) similarity
        item_similarity = cosine_similarity(self.user_item_matrix.T)
        item_similarity_df = pd.DataFrame(
            item_similarity,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )
        
        # Get movies user has rated
        user_rated_movies = self.user_item_matrix.loc[user_id]
        rated_movies = user_rated_movies[user_rated_movies > 0].index
        
        # Find similar movies
        recommendations = {}
        for rated_movie in rated_movies:
            similar_movies = item_similarity_df[rated_movie].sort_values(ascending=False)[1:6]
            rating = user_rated_movies[rated_movie]
            
            for similar_movie, similarity_score in similar_movies.items():
                if similar_movie not in rated_movies:
                    if similar_movie not in recommendations:
                        recommendations[similar_movie] = 0
                    recommendations[similar_movie] += similarity_score * rating
        
        # Sort by score and return top N
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [movie_id for movie_id, _ in sorted_recs[:n_recommendations]]
    
    def content_based_filtering(self, movie_id: int, n_recommendations: int = 5) -> List[int]:
        """
        Content-Based Filtering using genres and tags
        Find similar movies based on content features
        
        Args:
            movie_id: Target movie ID to find similar movies
            n_recommendations: Number of movies to recommend
            
        Returns:
            List of recommended movie IDs
        """
        if self.content_features is None or movie_id >= self.content_features.shape[0]:
            return []
        
        # Calculate content similarity
        content_similarity = cosine_similarity(self.content_features)
        similar_movies = content_similarity[movie_id].argsort()[::-1][1:n_recommendations+1]
        
        return [int(movie_id) for movie_id in similar_movies]
    
    def matrix_factorization(self, n_factors: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Matrix Factorization using NMF (Non-Negative Matrix Factorization)
        Factorize user-item matrix into user and item feature matrices
        
        Args:
            n_factors: Number of latent factors
            
        Returns:
            Tuple of (user_features, movie_features)
        """
        if self.user_item_matrix is None or self.user_item_matrix.empty:
            return np.array([]), np.array([])
        
        # Handle negative values by shifting
        matrix_shifted = self.user_item_matrix.values.copy()
        matrix_shifted[matrix_shifted < 0] = 0
        
        # Apply NMF
        self.nmf_model = NMF(n_components=n_factors, init='random', random_state=42, max_iter=300)
        self.user_features = self.nmf_model.fit_transform(matrix_shifted)
        self.movie_features = self.nmf_model.components_.T
        
        return self.user_features, self.movie_features
    
    def recommend_using_mf(self, user_id: int, n_recommendations: int = 5, 
                           user_index_map: Dict[int, int] = None) -> List[int]:
        """
        Get recommendations using Matrix Factorization
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of movies to recommend
            user_index_map: Mapping from user_id to index in matrix
            
        Returns:
            List of recommended movie IDs
        """
        if self.user_features is None or self.movie_features is None:
            return []
        
        # Get user index
        if user_index_map and user_id in user_index_map:
            user_idx = user_index_map[user_id]
        else:
            user_idx = user_id
        
        if user_idx >= self.user_features.shape[0]:
            return []
        
        # Calculate predicted ratings
        user_vector = self.user_features[user_idx]
        predicted_ratings = np.dot(user_vector, self.movie_features.T)
        
        # Get top N unrated movies
        if self.user_item_matrix is not None and user_id in self.user_item_matrix.index:
            user_rated = self.user_item_matrix.loc[user_id]
            predicted_ratings[user_rated > 0] = -np.inf
        
        top_movie_indices = np.argsort(predicted_ratings)[::-1][:n_recommendations]
        return [int(idx) for idx in top_movie_indices]
    
    def hybrid_recommendations(self, user_id: int, movie_id: int = None, 
                              n_recommendations: int = 5, weights: Dict = None) -> List[int]:
        """
        Hybrid Recommendation combining all methods
        
        Args:
            user_id: Target user ID
            movie_id: Optional movie ID for content-based filtering
            n_recommendations: Number of movies to recommend
            weights: Weights for different methods {'user_user': 0.3, 'item_item': 0.3, 'content': 0.2, 'mf': 0.2}
            
        Returns:
            List of recommended movie IDs
        """
        if weights is None:
            weights = {'user_user': 0.3, 'item_item': 0.3, 'content': 0.2, 'mf': 0.2}
        
        recommendations_score = {}
        
        # User-User Collaborative Filtering
        uu_recs = self.collaborative_filtering_user_user(user_id, n_recommendations * 2)
        for i, movie_id_rec in enumerate(uu_recs):
            score = (len(uu_recs) - i) / len(uu_recs) if uu_recs else 0
            recommendations_score[movie_id_rec] = recommendations_score.get(movie_id_rec, 0) + weights['user_user'] * score
        
        # Item-Item Collaborative Filtering
        ii_recs = self.collaborative_filtering_item_item(user_id, n_recommendations * 2)
        for i, movie_id_rec in enumerate(ii_recs):
            score = (len(ii_recs) - i) / len(ii_recs) if ii_recs else 0
            recommendations_score[movie_id_rec] = recommendations_score.get(movie_id_rec, 0) + weights['item_item'] * score
        
        # Matrix Factorization
        mf_recs = self.recommend_using_mf(user_id, n_recommendations * 2)
        for i, movie_id_rec in enumerate(mf_recs):
            score = (len(mf_recs) - i) / len(mf_recs) if mf_recs else 0
            recommendations_score[movie_id_rec] = recommendations_score.get(movie_id_rec, 0) + weights['mf'] * score
        
        # Content-Based (if movie_id provided)
        if movie_id:
            cb_recs = self.content_based_filtering(movie_id, n_recommendations * 2)
            for i, movie_id_rec in enumerate(cb_recs):
                score = (len(cb_recs) - i) / len(cb_recs) if cb_recs else 0
                recommendations_score[movie_id_rec] = recommendations_score.get(movie_id_rec, 0) + weights['content'] * score
        
        # Sort and return top N
        sorted_recs = sorted(recommendations_score.items(), key=lambda x: x[1], reverse=True)
        return [movie_id for movie_id, _ in sorted_recs[:n_recommendations]]
    
    def evaluate_recommendations(self, test_ratings: List[Dict], 
                                recommendations_func: callable, 
                                n_recommendations: int = 5) -> Dict:
        """
        Evaluate recommendation accuracy using precision, recall, RMSE
        
        Args:
            test_ratings: Test data with user_id, movie_id, rating
            recommendations_func: Function to get recommendations
            n_recommendations: Number of recommendations
            
        Returns:
            Dictionary with evaluation metrics
        """
        metrics = {
            'precision': [],
            'recall': [],
            'ndcg': [],
            'mae': [],
            'rmse': []
        }
        
        # Group test ratings by user
        test_df = pd.DataFrame(test_ratings)
        user_groups = test_df.groupby('user_id')
        
        for user_id, group in user_groups:
            # Get recommendations
            recs = recommendations_func(user_id, n_recommendations)
            
            if not recs:
                continue
            
            # Check which recommendations were rated
            relevant_movies = set(group[group['rating'] >= 4]['movie_id'].values)
            recommended_set = set(recs)
            
            # Precision: relevant items / recommended items
            if recommended_set:
                precision = len(relevant_movies & recommended_set) / len(recommended_set)
                metrics['precision'].append(precision)
            
            # Recall: relevant items / all relevant items
            if relevant_movies:
                recall = len(relevant_movies & recommended_set) / len(relevant_movies)
                metrics['recall'].append(recall)
            
            # Calculate NDCG and other metrics
            # ... (simplified for brevity)
        
        # Calculate averages
        result = {}
        for key in metrics:
            if metrics[key]:
                result[key] = np.mean(metrics[key])
            else:
                result[key] = 0.0
        
        return result
