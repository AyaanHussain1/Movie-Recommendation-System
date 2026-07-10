import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import nltk
from nltk.stem.porter import PorterStemmer
import streamlit as st

df = pd.read_csv("tmdb_5000_movies.xls")
df2 = pd.read_csv("tmdb_5000_credits.xls")

movies_data = df.merge(df2,on="title")
movies_data_pre_processing = movies_data[["movie_id","genres","keywords","overview","title","cast","crew"]]
# print(movies_data_pre_processing.isnull().sum())
movies_data_pre_processing["overview"] = movies_data_pre_processing["overview"].dropna().drop_duplicates()

class functions():
    def fetching_keywords_names(self,data_keyword):
        self.data = data_keyword
        name_list = []
        name_list.append([item["name"] for item in ast.literal_eval(self.data)])  # it evaluates a string containing a Python literal (like a list, dictionary, tuple, or string) and turns it into an actual, usable Python object.
        return name_list

    def cast_first_3(self,data_cast):
        self.data_c = data_cast
        cast_list = []
        cast_list.append([item["character"] for item in ast.literal_eval(self.data_c)[:3]])
        return cast_list
    
    def crew_depart_name(self,data_crew):
        self_crw = data_crew
        crew_list = []
        crew_list.append([[item["department"],item["name"]] for item in ast.literal_eval(self_crw)[:5]])
        return crew_list

    def getting_genres(self,data_genres):
        self.gen = data_genres
        genres_list = []
        genres_list.append([item["name"] for item in ast.literal_eval(self.gen)])
        return genres_list
    
    # only want 1 word not action or actio or else
    def stem(self,text):
        ps = PorterStemmer()
        self_t = text
        x = []
        for i in self_t.split():
            x.append(ps.stem(i))
        return " ".join(x)
    
    def recommend(self,movie):
        self_m = movie
        movie_index = movies_data_pre_processing[movies_data_pre_processing["title"] == self_m].index[0]
        distance = similarity[movie_index]
        movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
        
        recommend_movies = []
        recommend_movie_poster = []
        for i in movies_list:

            # print(movies_data_pre_processing.iloc[i[0]].title)
            movie_poster = movies_data_pre_processing.iloc[i[0]].movie_id
            recommend_movies.append(movies_data_pre_processing.iloc[i[0]].title)
            recommend_movie_poster.append(self.fetch_poster(movie_poster))

        return recommend_movies,recommend_movie_poster

    def fetch_poster(self,movie_poster):
        self_mp = movie_poster
        response =  requests.get(f"https://api.themoviedb.org/3/movie/{self_mp}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

func = functions()
movies_data_pre_processing["keywords"] = movies_data_pre_processing["keywords"].apply(func.fetching_keywords_names)
# print(f"Keywords : {movies_data_pre_processing["keywords"].head(2)}\n")

movies_data_pre_processing["genres"] = movies_data_pre_processing["genres"].apply(func.getting_genres)
# print(f"Genres : {movies_data_pre_processing["genres"].head(2)}\n")

movies_data_pre_processing["cast"] = movies_data_pre_processing["cast"].apply(func.cast_first_3)
# print(f"Cast : {movies_data_pre_processing["cast"].head(2)}\n")

movies_data_pre_processing["crew"] = movies_data_pre_processing["crew"].apply(func.crew_depart_name)
# print(f"Crew : {movies_data_pre_processing["crew"].head(2)}")

movies_data_pre_processing["overview"] = movies_data_pre_processing["overview"].apply(lambda x:str(x).split())
movies_ready_data = movies_data_pre_processing["overview"] + movies_data_pre_processing["genres"] + movies_data_pre_processing["keywords"] + movies_data_pre_processing["cast"] + movies_data_pre_processing["crew"]
movies_data_pre_processing["tags"] = movies_ready_data.apply(lambda x: " ".join([str(item) for item in x]))
movies_data_pre_processing["tags"] = movies_data_pre_processing["tags"].apply(lambda x: x.lower())
movies_data_pre_processing = movies_data_pre_processing.drop(columns=["overview","genres","keywords","cast","crew"])

# only want 1 word not action or actio or else
movies_data_pre_processing["tags"] = movies_data_pre_processing["tags"].apply(func.stem) 

# movies_data_pre_processing.to_csv("movies_ready_data_for_model.csv")

# Now mathcing Results

cv = CountVectorizer(max_features=5000,stop_words="english")
vectors = cv.fit_transform(movies_data_pre_processing["tags"]).toarray()
# print(vectors[1221])

similarity = cosine_similarity(vectors)
# sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

# checking
# func.recommend("Pirates of the Caribbean: At World's End")

st.title("Movie Recommendation System")
selected_movie = st.selectbox(
    'What Movies Would You Like To Watch?',
    (movies_data_pre_processing["title"].values)
)

if st.button("Recommend"):
    names, posters = func.recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
