import streamlit as st
import pickle
import pandas as pd

def load_data():
    try:
        movies_dict = pickle.load(open('movie.dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error("Failed to load data: " + str(e))
        return None, None

def recommend(movie, movies, similarity):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [movies.iloc[i[0]].title for i in movie_list]
        return recommended_movies
    except Exception as e:
        st.error("Failed to generate recommendations: " + str(e))
        return []

def main():
    st.title("Movie Recommendation System")
    
    movies, similarity = load_data()
    if movies is None or similarity is None:
        return
    
    selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

    if st.button('Recommend'):
        recommendations = recommend(selected_movie_name, movies, similarity)
        if recommendations:
            st.write("Recommended Movies:")
            for movie in recommendations:
                st.write(movie)

if __name__ == "__main__":
    main()
