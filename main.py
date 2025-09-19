"""
Main CLI Application for Personal Movie Database

This application allows users to manage a personal movie collection
through a command-line interface (CLI) with persistent storage
and web integration.

Features:
- List all movies in the database
- Add a new movie via OMDb API (automatic details) or manually
- Delete an existing movie by title
- Update movie rating and/or year
- View statistics: average and median ratings, best and worst movies
- Get a random movie recommendation
- Search for movies by partial title match
- Sort movies by rating or release year
- Persistent storage using SQLite database for all movie data
- Static HTML generation for displaying movies in a web page
- Robust input validation, error handling, and user-friendly feedback

This application integrates SQL, API fetching, and HTML generation
to provide a modern and versatile personal movie management tool.

Intended for educational and personal use.
"""

from colorama import init
from movie_helpers import welcome, get_user_choice, exit_app
from movie_operations import (
    initialize_app_data,
    list_movies,
    add_movie,
    delete_movie,
    update_movie,
    random_movie,
    search_movie,
)
from movie_stats import stats, movies_sorted_by_rating, movies_sorted_by_year
from website_generator import generate_website

# Initialize colorama
init()


def execute_user_action(user_action, movies):
    """Execute the function corresponding to user's menu choice"""
    actions = {
        0: exit_app,
        1: list_movies,
        2: add_movie,
        3: delete_movie,
        4: update_movie,
        5: stats,
        6: random_movie,
        7: search_movie,
        8: movies_sorted_by_rating,
        9: movies_sorted_by_year,
        10: generate_website,
    }

    if user_action == 0:
        exit_app()
    elif user_action == 10:
        generate_website()
    else:
        actions[user_action](movies)


def control_logic():
    """Main application control loop"""
    movies = initialize_app_data()

    while True:
        user_choice = get_user_choice()
        execute_user_action(user_choice, movies)


def main():
    """Entry point of the application"""
    welcome()
    control_logic()


if __name__ == "__main__":
    main()
