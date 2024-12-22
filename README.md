# 🎬 MovieLens Recommendation System

A Streamlit-based web application that provides movie recommendations using the MovieLens 100K dataset and TMDB API.

## Access at https://movie-lens-recommender.streamlit.app

## Features
- Movie recommendations based on user selection
- Detailed movie information including directors, release dates, and genres
- Movie poster images from TMDB
- Interactive web interface
- Similarity-based recommendation algorithm

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MovieLensRecommendation.git
cd MovieLensRecommendation
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a secrets.toml file and add your TMDb API key:
```toml
tmdb_api_key = "your-api-key-here"
```

## Usage
Run the Streamlit app through your terminal:
```bash
streamlit run app.py
```

## Data Source
This project uses the MovieLens 100K Dataset, which contains 100,000 movie ratings from 943 users on 1,682 movies.

## Dependencies
streamlit==1.31.0
pandas==2.1.4
tmdbv3api==1.9.0
numpy==1.26.3

## Project Structure
MovieLensRecommendation/
├── .streamlit/
│   └── secrets.toml
├── ml-100k/
│   ├── u.data
│   └── u.item
├── movielens_project.py
├── app.py
└── requirements.txt

## MIT License

Copyright (c) 2024 Tal Berry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
