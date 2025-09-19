"""
website_generator.py

Generates an HTML website for movies using data fetched from the sql
"""

import os
from sqlalchemy import create_engine, text

# Define the database URI
DB_URL = "sqlite:///movies.db"
# Movie image placeholder
IMAGE_PLACEHOLDER = "https://placehold.jp/150x150.png"

# Create Engine
engine = create_engine(DB_URL, echo=True)


# 1. Read the contents of the template, index_template.html
def read_html_template(template_path):
    """
    Reads an HTML template from a file.

    :param template_path: Path to the HTML template file.
    :return: Content of the template file as a string.
    """
    with open(template_path, "r", encoding="utf-8") as fileobject:
        return fileobject.read()


def serialize_movies_data(movies_data):
    """
    serializes the list of movie data into HTML list items,
    skipping any missing fields.

    :param movies_data: List of movie data dictionaries.

    :param movies_data:
    :return: A string containing the HTML representation of the movies' data.
    """
    output = ""
    for movie in movies_data:
        output += f'<li class="movie-item">\n'
        poster_path = "placeholder_image.png"
        poster = movie.get("poster_url")
        if not poster:
            poster = poster_path
        elif not poster.startswith(("http://", "https://")) and not os.path.exists(
            poster
        ):
            poster = poster_path
        output += (
            f'    <img class = "movie-poster" src = "{poster or poster_path}" '
            f'alt = "{movie.get("title", "")}">\n'
        )
        output += f'    <h3>{movie.get("title", "")}</h3>\n'
        output += f'    <p>{movie.get("year", "")}</p>\n'
        output += f'    <p>{movie.get("rating", "")}</p>\n'
        output += "</li>\n"
    return output


# Step 3. Write this new string to the 'new' html file
def write_html_template(html_data):
    """
    Writes the given HTML content (str) to the 'movies.html' file.

    :param html_data: A string containing the full HTML content (str)
    to be written to the file.
    :return: None
    """
    with open("movies.html", "w", encoding="utf-8") as fileobject:
        fileobject.write(html_data)


def generate_website():
    """
    Generate the movies HTML website.

    Reads the HTML template, fills it with movie data from the database,
    and writes the final HTML to 'movies.html'.
    """
    movies_from_database = []
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT * FROM movies"""))
        for row in result:
            movies_dict = {
                "title": row[1],
                "year": row[2],
                "rating": row[3],
                "poster_url": row[4],
            }
            movies_from_database.append(movies_dict)
    # Read HTML template
    movies_template_path = "index_template.html"
    movies_template_html = read_html_template(movies_template_path)
    print(movies_template_html)

    # Step 3:
    final_html = movies_template_html.replace(
        "__TEMPLATE_TITLE__", "My Movie App"
    ).replace("__TEMPLATE_MOVIE_GRID__", serialize_movies_data(movies_from_database))
    print(final_html)
    write_html_template(final_html)
