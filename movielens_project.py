import pandas as pd

ratings = pd.read_csv('./ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

movies = pd.read_csv('./ml-100k/u.item', sep='|', encoding='latin_1', header=None, names=['movie_id', 'title'], usecols=[0, 1])

print("Ratings Data:")
print(ratings.head)

print("\nMovies Data:")
print(movies.head)