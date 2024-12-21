import streamlit as st
from movielens_project import load_data, create_similarity_matrix, movie_rec, get_movie_details

def main():
    st.title("🎬 Movielens100K Movie Recommendation System", anchor=False)
    
    # Load data and create similarity matrix
    @st.cache_data
    def load_cached_data():
        ratings, movies = load_data()
        similarity, matrix = create_similarity_matrix(ratings, movies)
        return ratings, movies, similarity, matrix
    
    ratings, movies, similarity, matrix = load_cached_data()
        
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
                with st.expander("Movie Details", expanded=True):
                    st.write(f"Release Date: {input_movie_details['release_date']}")
                    st.write(f"Genres: {', '.join(input_movie_details['genres'])}")
                    if input_movie_details['tmdb_url']:
                        st.markdown(f"[View on TMDb]({input_movie_details['tmdb_url']})")
                
                # Display recommendations
                for i, (movie, score) in enumerate(recommendations.items(), 1):
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        details = get_movie_details(movie, movies)
                        with col1:
                            if details['poster'] and details['tmdb_url']:
                                st.markdown("""
                                <style>
                                .poster {
                                    border-radius: 10px;
                                    box-shadow: 0px 0px 5px 2px rgba(80, 80, 80, 0.3);
                                    width: 150px;
                                    position: relative;
                                    top: -2px;
                                    transition: transform 0.5s ease, box-shadow 0.5s ease;
                                }
                                
                                .poster:hover {
                                    transform: scale(1.05);
                                    box-shadow: 0px 0px 15px 5px rgba(80, 80, 80, 0.4);
                                }
                                </style>
                                """, unsafe_allow_html=True)
                                st.markdown(
                                    f"""
                                    <a href="{details['tmdb_url']}" target="_blank" title="View on TMDb">
                                    <img class='poster' src='{details['poster']}'/>
                                    </a>
                                    """, unsafe_allow_html=True)
                        with col2:
                            st.write(f"**{details['title']}**")
                            st.write(f"Similarity Score: {score:.2f}")
                            st.write(f"Release Date: {details['release_date']}")
                            st.write(f"Genres: {', '.join(details['genres'])}")
                        st.divider()
            else:
                st.error("Movie not found in database!")
        else:
            st.warning("Please select a movie!")

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