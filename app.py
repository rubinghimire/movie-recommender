import argparse
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify


app = Flask(__name__)
app.debug = True


def load_data():
    movies_df = pd.read_csv('data/movies.csv')
    ratings_df = pd.read_csv('data/ratings.csv')
    return movies_df, ratings_df


@app.route('/')
def index():
    return "Welcome to the Movie Recommender!"


def find_movie_in_database(movies_df, movie_name):
    return movies_df[movies_df['title'].str.lower() == movie_name.lower()]


def find_similar_movies(movies_df, movie_name):
    movie_name_words = set(movie_name.lower().split())
    similar_movies = []

    for _, row in movies_df.iterrows():
        title_words = set(row['title'].lower().split())
        similarity_score = len(movie_name_words.intersection(title_words))
        similar_movies.append((row['title'], similarity_score))

    similar_movies.sort(key=lambda x: x[1], reverse=True)
    return similar_movies[:5]


def recommend_movies(ratings_df, movie_name):
    movie_ratings = ratings_df[ratings_df['title'] == movie_name]
    if movie_ratings.empty:
        return []

    movie_ratings = movie_ratings.sort_values(by='rating', ascending=False)
    top_users = movie_ratings.iloc[:5]['userId'].values
    recommended_movies = []

    for user_id in top_users:
        user_ratings = ratings_df[(ratings_df['userId'] == user_id) & (ratings_df['title'] != movie_name)]
        user_ratings = user_ratings.sort_values(by='rating', ascending=False)
        recommended_movies.extend(user_ratings.iloc[:5]['title'].values)

    return recommended_movies


@app.route("/recommend/<movie_name>")
def recommend_movies_based_on_genres(movie_name):
    movies_df, ratings_df = load_data()
    movie_in_db = find_movie_in_database(movies_df, movie_name)

    if movie_in_db.empty:
        similar_movies = find_similar_movies(movies_df, movie_name)
        similar_movie_titles = [title for title, _ in similar_movies]
        return jsonify({"recommendations": similar_movie_titles})
    else:
        recommended_movies = recommend_movies(ratings_df, movie_name)

        def score_movie(movie):
            movie_genres = set(movie['genres'].split('|'))
            given_movie_genres = set(movie_in_db.iloc[0]['genres'].split('|'))
            return len(given_movie_genres.intersection(movie_genres))

        recommended_movies.sort(key=lambda movie: score_movie(movies_df[movies_df['title'] == movie]), reverse=True)
        return jsonify({"recommendations": recommended_movies})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_name', help='the title of the movie you like, from the list "data/movies.csv"')
    args = parser.parse_args()

    app.run(debug=True)
