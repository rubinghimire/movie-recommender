import argparse
import numpy as np
import pandas as pd
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True


def load_data():
    # Reading csv into dataframes
    movies_df = pd.read_csv('data/movies.csv')
    ratings_df = pd.read_csv('data/ratings.csv')
    return movies_df, ratings_df


@app.route('/')
def root():
    return "Welcome to the Movie Recommender!"


@app.route('/recommend')
@app.route('/recommend/')
def recommend():
    return "Please use /recommend/movie_title to get recommendations."


def find_movie_in_dataframe(movies_df, movie_name):
    matching_movies = movies_df[movies_df['title'] == movie_name]
    print(f'matching movies {matching_movies}')
    if not matching_movies.empty:
        # Return the first matching movie found
        return matching_movies.iloc[0]
    else:
        return None
    # return movies_df[movies_df['title'].str.lower() == movie_name.lower()]


def find_similar_movies(movies_df, ratings_df, movie_name):
    movie_name_words = set(movie_name.lower().split())
    # A list of tuples
    similar_movies = []

    # Iterate over movies_df; unconcerned with row index
    # concerned with just the row (hence the _, row)
    for _, row in movies_df.iterrows():
        # Sets have a faster lookup time compared for lists or dictionaries
        # Sets are optimized for intersection, union, etc operations
        title_words = set(row['title'].lower().split())
        # Assign count of common words to similarity_score
        similarity_score = len(movie_name_words.intersection(title_words))
        similar_movies.append((row['title'], similarity_score))

    similar_movies.sort(key=lambda x: x[1], reverse=True)
    return similar_movies[:10]


def recommend_movies(merged_df, movie_name):
    # Retrieve multiple entries of the given movie in the df
    movies = merged_df[merged_df['title'] == movie_name]
    if movies.empty:
        return []
    # Sort the values of the movies df in descending order based on rating
    # Assign to movie_ratings
    movie_ratings = movies.sort_values(by='rating', ascending=False)
    # Select the top five users who have given the highest rating to the given movie
    top_users = movie_ratings.iloc[:5]['userId'].values
    # Instantiate an empty list to store recommended movies
    recommended_movies = []

    for user_id in top_users:
        # Get rows (df) where ratings are by current user
        user_ratings = merged_df[(merged_df['userId'] == user_id)]
        # Sort the rows (df) by the highest rating first
        user_ratings = user_ratings.sort_values(by='rating', ascending=False)
        # Add the top five movies for the current user to the recommended_movies list
        recommended_movies.extend(user_ratings.iloc[:5]['title'].values)

    # Remove duplicate recommendations from the list
    recommended_movies = np.unique(recommended_movies)
    return recommended_movies


@app.route("/recommend/<movie_name>", methods=['GET', 'OPTIONS'])
def recommend_movies_based_on_genres(movie_name):
    # Handle OPTIONS requests and providing the necessary CORS headers
    # Helps client determine the allowed HTTP methods
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response

    # Load the files into movies and ratings dataframes (unpack tuple)
    # Get the movie (df) sent by the user in movie dataframe
    movies_df, ratings_df = load_data()
    movie_in_df = find_movie_in_dataframe(movies_df, movie_name)

    # If movie is not found in dataframe, find similar movies
    # Else: call recommend_movies() and store result in recommended_movies (list)
    if movie_in_df is None:
        similar_movies = find_similar_movies(movies_df, ratings_df, movie_name)
        # Unpack the similar_movies tuples and store title for each movie
        # Assign list of titles to similar_movie_titles
        similar_movie_titles = [title for title, _ in similar_movies]
        return jsonify({"recommendations": similar_movie_titles})
    else:
        print(f'inside recommend_movies')
        merged_df = movies_df.merge(ratings_df, on="movieId")
        recommended_movies = recommend_movies(merged_df, movie_name)

    # Calculate a score for a movie based on similarity of
    # genres between the recommended movie and specified movie
    def score_movie(movie, specified_movie_genres):
        movie_genres = set(movie['genres'].split('|'))
        return len(specified_movie_genres.intersection(movie_genres))

    # Dictionary to store movie scores
    scores = {}

    # Calculate the score for each recommended_movie
    for recommended_movie in recommended_movies:
        score = score_movie(movies_df[movies_df['title']
                                      == recommended_movie].iloc[0],
                            set(movie_in_df['genres'].split('|')))
        # Store the score in scores dictionary
        scores[recommended_movie] = score

    # Retrieve the score for each movie in recommended_movies list
    # and use that as basis for sorting (order: highest to lowest score)
    recommended_movies = sorted(recommended_movies, key=lambda x: scores.get(x, 0), reverse=True)

    # Return the list as JSON
    return jsonify({"recommendations": recommended_movies})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_name', help='the title of the movie you like"')
    args = parser.parse_args()

    app.run(debug=True)
