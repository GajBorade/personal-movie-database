from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT NOT NULL
        )
    """
        )
    )
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT title, year, rating, poster_url " "FROM movies")
        )
        movies = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }


def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database."""
    with engine.connect() as conn:
        try:
            conn.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster_url) "
                    "VALUES (:title, :year, :rating, :poster_url)"
                ),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url,
                },
            )
            conn.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as conn:
        try:
            conn.execute(
                text("DELETE FROM movies WHERE title = :title"), {"title": title}
            )
            conn.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, year, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as conn:
        try:
            conn.execute(
                text(
                    "UPDATE movies SET year = :year, rating = :rating"
                    " WHERE (title = :title)"
                ),
                {"title": title, "year": year, "rating": rating},
            )
            conn.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
