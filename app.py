import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os
if not os.path.exists('similarity.pkl'):
    # run your notebook preprocessing here
    pass


if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/uc?id=1W3hU1TMc9q4ZG76FG3A26tGu3Bscufhj'
    gdown.download(url, 'similarity.pkl', quiet=False)
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={
                "api_key": "600a722bc188c9ed28eaeb164ff22c00",
                "language": "en-US"
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            timeout=10
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://placehold.co/500x750?text=No+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])