import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database import get_db_connection

class Recommender:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads data from the database and retrains the model."""
        conn = get_db_connection()
        try:
            self.df = pd.read_sql_query("SELECT * FROM books", conn)
            if not self.df.empty:
                # Fill missing values
                self.df['title'] = self.df['title'].fillna('Unknown Title')
                self.df['author'] = self.df['author'].fillna('Unknown Author')
                self.df['description'] = self.df['description'].fillna('')
                
                # Combine Title and Description for better matching
                self.df['combined_text'] = self.df['title'] + " " + self.df['description']
                self.df['combined_text'] = self.df['combined_text'].apply(
                    lambda x: x.replace("Description unavailable.", "").replace("Description loading...", "")
                )
                
                self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
                self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_text'])
                
                print(f"Recommender loaded with {len(self.df)} books.")
            else:
                print("No books found in DB.")
        except Exception as e:
            print(f"Error loading data for recommender: {e}")
        finally:
            conn.close()

    def recommend(self, query, top_n=10):
        """Recommend books based on a natural language query."""
        if self.vectorizer is None or self.tfidf_matrix is None:
            self.load_data()
            if self.vectorizer is None:
                return []
        
        try:
            query_vec = self.vectorizer.transform([query])
            cosine_sim = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Get top N indices with non-zero scores
            top_indices = cosine_sim.argsort()[-top_n:][::-1]
            
            results = []
            for idx in top_indices:
                if cosine_sim[idx] > 0:
                    book = self.df.iloc[idx].to_dict()
                    book['match_score'] = float(cosine_sim[idx])
                    results.append(book)
                    
            return results
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return []

    def get_similar_books(self, isbn, top_n=5):
        """Find books similar to a specific book given by ISBN."""
        if self.df is None or self.tfidf_matrix is None:
            return []
            
        try:
            # Find the index of the book
            idx_list = self.df.index[self.df['isbn'] == isbn].tolist()
            if not idx_list:
                return []
            
            idx = idx_list[0]
            # Calculate similarity on the fly for this specific book only
            # This saves massive amounts of RAM (prevents exit code 137)
            target_vec = self.tfidf_matrix[idx]
            sim_scores = cosine_similarity(target_vec, self.tfidf_matrix).flatten()
            
            # Sort by similarity, skip the first one as it's the book itself
            sim_scores_idx = sim_scores.argsort()
            # Get top N+1 indices (last N+1 elements since argsort is ascending)
            top_indices = sim_scores_idx[-(top_n+1):-1][::-1]
            
            results = []
            for i in top_indices:
                if sim_scores[i] > 0:
                    book = self.df.iloc[i].to_dict()
                    results.append(book)
                
            return results
        except Exception as e:
            print(f"Error getting similar books: {e}")
            return []

    def get_books_by_author(self, author_name, skip_isbn=None, top_n=5):
        """Find more books by the same author."""
        if self.df is None:
            return []
            
        try:
            # Simple substring match for author
            matches = self.df[self.df['author'].str.contains(author_name, case=False, na=False)]
            
            if skip_isbn:
                matches = matches[matches['isbn'] != skip_isbn]
                
            results = matches.head(top_n).to_dict('records')
            return results
        except Exception as e:
            print(f"Error getting books by author: {e}")
            return []

# Global instance
recommender = Recommender()
