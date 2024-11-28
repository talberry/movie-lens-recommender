import pandas as pd
import numpy as np

def load_data():
    # Load ratings data
    ratings = pd.read_csv('ml-100k/u.data', 
                         sep='\t', 
                         names=['user_id', 'movie_id', 'rating', 'timestamp'])
    
    # Load movie data
    movies = pd.read_csv('ml-100k/u.item', 
                        sep='|', 
                        encoding='latin-1',
                        names=['movie_id', 'title', 'release_date', 'video_release_date',
                              'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                              'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                              'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                              'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
    
    return ratings, movies

def create_similarity_matrix(ratings, movies):
    # Merge ratings and movies data
    merged = pd.merge(ratings, movies, on='movie_id')
    
    # Create utility matrix (user-movie ratings matrix)
    matrix = merged.pivot_table(index='user_id', columns='title', values='rating')
    
    # Calculate similarity matrix using Pearson correlation
    similarity = matrix.corr(method='pearson')
    
    return similarity, matrix

def movie_rec(title, similarity, num_recs=5):
    """
    Get movie recommendations based on movie title
    
    Parameters:
    title (str): Movie title to base recommendations on
    similarity (DataFrame): Movie similarity matrix
    num_recs (int): Number of recommendations to return
    
    Returns:
    Series: Series of recommended movies with similarity scores
    """
    if title not in similarity:
        print(f"'{title}' is not in the movie list.")
        return None
    
    # Get similar movies and sort them
    similar_movs = similarity[title].dropna().sort_values(ascending=False)
    
    # Remove the input movie from recommendations
    similar_movs = similar_movs.drop(title, errors='ignore')
    
    return similar_movs.head(num_recs)

def get_movie_genres(movie_title, movies_df):
    """Get genres for a specific movie"""
    genre_columns = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 
                    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 
                    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
                    'Thriller', 'War', 'Western']
    
    movie_row = movies_df[movies_df['title'] == movie_title]
    if not movie_row.empty:
        genres = [genre for genre in genre_columns if movie_row.iloc[0][genre] == 1]
        return genres
    return []

def get_movie_details(movie_title, movies_df):
    """Get detailed information about a movie"""
    movie_info = movies_df[movies_df['title'] == movie_title].iloc[0]
    return {
        'title': movie_info['title'],
        'release_date': movie_info['release_date'],
        'genres': get_movie_genres(movie_title, movies_df),
        'imdb_url': movie_info['IMDb_URL']
    }

if __name__ == "__main__":
    # Load data
    ratings, movies = load_data()
    
    # Create similarity matrix
    similarity, matrix = create_similarity_matrix(ratings, movies)
    
    print("Utility Matrix:")
    print(matrix.head())
    
    print("\nMovie Similarities:")
    print(similarity.head())
    
    # Get recommendations for Star Wars
    recommended_movies = movie_rec("Star Wars (1977)", similarity)
    
    print("\nRecommended Movies:")
    print(recommended_movies)
    
    # Example of getting movie details
    if recommended_movies is not None:
        print("\nDetailed Recommendations:")
        for movie in recommended_movies.index:
            details = get_movie_details(movie, movies)
            print(f"\nTitle: {details['title']}")
            print(f"Release Date: {details['release_date']}")
            print(f"Genres: {', '.join(details['genres'])}")
            print(f"IMDb: {details['imdb_url']}")

