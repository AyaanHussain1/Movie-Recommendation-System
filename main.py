import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_poster):
   
   response =  requests.get(f"https://api.themoviedb.org/3/movie/{movie_poster}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
   data = response.json()
   return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    recommend_movie_tag = []

    for i in movies_list:

        movie_poster = movies.iloc[i[0]].id 
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movie_tag.append(movies.iloc[i[0]].tags)

          # movie poster fetching

        recommend_movies_poster.append(fetch_poster(movie_poster))

    return recommend_movies,recommend_movies_poster,recommend_movie_tag

similarity = pickle.load(open("similarity.pkl","rb"))
movies_list = pickle.load(open("movies.pkl","rb"))

movies = pd.DataFrame(movies_list)

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    'What Movies Would You Like TO Watch?',
    (movies["title"].values)
)
if st.button("Recommend"):
    names,posters,tags= recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Place content into each column dynamically
    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.caption(tags[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.caption(tags[1])
        
    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.caption(tags[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.caption(tags[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.caption(tags[4])