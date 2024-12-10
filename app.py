import streamlit as st
from tmdbv3api import TMDb, Movie
from dotenv import load_dotenv
import os
from movielens_project import load_data, create_similarity_matrix, movie_rec, get_movie_details

load_dotenv()

tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY')

def main():
    st.title("🎬 Movie Recommendation System")
    
    # Load data and create similarity matrix
    # Using @st.cache_data to prevent recomputing on every rerun
    @st.cache_data
    def load_cached_data():
        ratings, movies = load_data()
        similarity, matrix = create_similarity_matrix(ratings, movies)
        return ratings, movies, similarity, matrix
    
    ratings, movies, similarity, matrix = load_cached_data()
    
    # Add a sidebar with movie stats
    st.sidebar.header("Dataset Statistics")
    st.sidebar.write(f"Total Movies: {len(movies)}")
    st.sidebar.write(f"Total Ratings: {len(ratings)}")
    st.sidebar.write(f"Total Users: {ratings['user_id'].nunique()}")
    
    # Main search/input area
    st.write("### Find Movies You'll Love")
    
    # Create a dropdown with all movie titles
    movie_titles = sorted(similarity.columns.tolist())
    movie_input = st.selectbox("Select a movie you like:", movie_titles)
    
    num_recommendations = st.slider("Number of recommendations:", 
                                  min_value=1, 
                                  max_value=20, 
                                  value=5)
    
    if st.button("Get Recommendations"):
        if movie_input:
            with st.spinner('Finding recommendations...'):
                recommendations = movie_rec(movie_input, similarity, num_recommendations)
            
            if recommendations is not None:
                st.write("### Recommended Movies:")
                st.info(f"Based on your interest in: {movie_input}")
                
                # Get details of the input movie
                input_movie_details = get_movie_details(movie_input, movies)
                with st.expander("Selected Movie Details", expanded=True):
                    st.write(f"**Release Date:** {input_movie_details['release_date']}")
                    st.write(f"**Genres:** {', '.join(input_movie_details['genres'])}")
                    st.write(f"[View on IMDb]({input_movie_details['imdb_url']})")
                
                # Display recommendations
                for i, (movie, score) in enumerate(recommendations.items(), 1):
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.write(f"#{i}")
                        with col2:
                            details = get_movie_details(movie, movies)
                            st.write(f"**{details['title']}**")
                            st.write(f"Similarity Score: {score:.2f}")
                            st.write(f"Release Date: {details['release_date']}")
                            st.write(f"Genres: {', '.join(details['genres'])}")
                            st.write(f"[View on IMDb]({details['imdb_url']})")
                        st.divider()
            else:
                st.error("Movie not found in database!")
        else:
            st.warning("Please select a movie!")

    # Genre filter in sidebar
    st.sidebar.header("Genre Statistics")
    genre_columns = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
                    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                    'Thriller', 'War', 'Western']
    
    # Count movies per genre
    genre_counts = {genre: movies[genre].sum() for genre in genre_columns}
    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
        st.sidebar.write(f"{genre}: {count} movies")

    # About section
    with st.expander("About this app"):
        st.write("""
        This movie recommendation system uses collaborative filtering with Pearson 
        correlation to suggest movies you might enjoy. The system analyzes how users 
        rate different movies and finds movies that have similar rating patterns to 
        the one you selected.
        
        The similarity score ranges from -1 to 1:
        - 1: Perfect positive correlation
        - 0: No correlation
        - -1: Perfect negative correlation
        
        Dataset: MovieLens 100k
        - Contains 100,000 ratings
        - From 943 users
        - On 1,682 movies
        - Rating scale: 1-5
        """)

if __name__ == "__main__":
    main() 