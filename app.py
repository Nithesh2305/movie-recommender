import streamlit as st
import pandas as pd
import requests
import pickle
import os
import time

# --------- Function to Download Files from Google Drive ---------
def download_file(url, filename):
    if not os.path.exists(filename):
        try:
            st.info(f"Downloading {filename} ...")
            response = requests.get(url)
            with open(filename, 'wb') as f:
                f.write(response.content)
            st.success(f"{filename} downloaded successfully.")
        except Exception as e:
            st.error(f"Failed to download {filename}: {e}")

# --------- Google Drive File Links (Replace with your actual file IDs) ---------
MOVIE_PKL_URL = "https://drive.google.com/uc?export=download&id=1uThfklSmAEp8pt040T8uj8edUboBHooR"
CREDITS_CSV_URL = "https://drive.google.com/uc?export=download&id=1lOZn0nWIEDi0qIULkHuauwt3ylGuzxeC"
MOVIES_CSV_URL = "https://drive.google.com/uc?export=download&id=1Va8IoUav-nbB-nWLesN2hTd2Q0iVizIY"

# --------- Download and Load Data ---------
download_file(MOVIE_PKL_URL, 'movie_data.pkl')
download_file(CREDITS_CSV_URL, 'tmdb_5000_credits.csv')
download_file(MOVIES_CSV_URL, 'tmdb_5000_movies.csv')

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Optional: Load raw CSVs (if needed for debugging or UI)
credits_df = pd.read_csv('tmdb_5000_credits.csv')
movies_df = pd.read_csv('tmdb_5000_movies.csv')

# --------- Recommendation Function ---------
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# --------- TMDB Poster Fetching ---------
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
    }
    attempts = 3
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except Exception as e:
            print(f"Error fetching poster for movie_id={movie_id} (attempt {attempt + 1}): {e}")
            time.sleep(1)
    return "https://via.placeholder.com/500x750?text=No+Image"

# --------- Streamlit UI ---------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.caption(movie_title)
