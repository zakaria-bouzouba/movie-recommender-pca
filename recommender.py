import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class PCARecommender:
    def __init__(self, data_path='data/ml-latest-small'):
        self.movies_path = os.path.join(data_path, 'movies.csv')
        self.ratings_path = os.path.join(data_path, 'ratings.csv')
        self.model_path = 'pca_model.pkl'
        self.data = None
        self.similarity_matrix = None
        self.indices = None

    def load_and_prep(self):
        """Loads data and creates the User-Item Matrix."""
        print("Loading data...")
        movies = pd.read_csv(self.movies_path)
        ratings = pd.read_csv(self.ratings_path)

        # Merge and create Pivot Table: Rows=Movies, Cols=Users
        df = pd.merge(ratings, movies, on='movieId')
        
        # Create a pivot matrix (Movies x Users)
        # Fill NaN with 0 (implying no rating/neutral)
        movie_user_mat = df.pivot_table(index='title', columns='userId', values='rating').fillna(0)
        
        return movie_user_mat

    def train(self, n_components=20):
        """Applies PCA and calculates Cosine Similarity."""
        matrix = self.load_and_prep()
        
        # Apply PCA
        # We reduce the ~600 users down to 'n' principal components
        print(f"Training PCA with {n_components} components...")
        pca = PCA(n_components=n_components)
        pca_fit = pca.fit_transform(matrix)
        
        # Calculate Cosine Similarity on the reduced matrix
        self.similarity_matrix = cosine_similarity(pca_fit)
        
        # Map movie titles to matrix indices for fast lookup
        self.indices = pd.Series(matrix.index)
        
        # Save artifacts (Simulated persistence)
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.similarity_matrix, self.indices), f)
        
        print("Training complete.")

    def load_model(self):
        """Loads pre-trained matrices."""
        if not os.path.exists(self.model_path):
            self.train()
        else:
            with open(self.model_path, 'rb') as f:
                self.similarity_matrix, self.indices = pickle.load(f)

    def recommend(self, title, k=5):
        """Returns top k similar movies."""
        try:
            # Case insensitive search
            idx = self.indices[self.indices.str.lower() == title.lower()].index[0]
        except IndexError:
            return None # Movie not found

        # Get similarity scores for this movie
        scores = list(enumerate(self.similarity_matrix[idx]))
        
        # Sort by score (descending)
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get top k (excluding the movie itself at index 0)
        top_indices = [i[0] for i in scores[1:k+1]]
        
        return self.indices.iloc[top_indices].tolist()

if __name__ == "__main__":
    # Test run
    rec = PCARecommender()
    rec.train()
    print("Test Recommendation for 'Toy Story (1995)':", rec.recommend('Toy Story (1995)'))