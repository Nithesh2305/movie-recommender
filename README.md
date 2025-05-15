🎬 Movie Recommender System
A content-based movie recommender system built with Python, Pandas, and Streamlit. Select your favorite movie from the dropdown list and get the top 10 similar movie recommendations along with their posters.

🚀 Features
Content-based filtering using cosine similarity

Simple and interactive Streamlit UI

Movie posters fetched using the TMDb API

📦 Installation
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
2. Create a Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

🧠 Usage
1. Run the Streamlit App

streamlit run app.py
2. Open Your Browser
Go to: http://localhost:8501

📌 How to Use
Select a movie from the dropdown menu.

Click the "Recommend" button.

View the top 10 recommended movies along with their posters.

🛠️ Requirements
Python 3.7+
pandas==2.2.2
Requests==2.32.3
streamlit==1.35.0

Dataset
The dataset used for this project contains information about movies, including their titles and IDs. It is processed and stored in movie_data.pkl. The dataset is used to calculate the cosine similarity between movies.Run whole ipynb to get movie_data.pkl .the datset used in this project can be found here
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata


Model
The model for recommending movies is based on cosine similarity. Cosine similarity is used to measure the similarity between movie titles. The model computes the similarity scores and suggests the top 10 similar movies based on the selected movie title.

