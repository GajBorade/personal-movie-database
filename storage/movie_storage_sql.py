from sqlalchemy import create_engine, text

# Define the database URL
import os
project_root = os.path.dirname(os.path.abspath(__file__))  # storage directory
project_root = os.path.dirname(project_root)  # go up to project root
DB_URL = f"sqlite:///{os.path.join(project_root, 'data', 'movies.db')}"

# Create the engine
engine = create_engine(DB_URL, echo=True)


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT title, year, rating, poster_url FROM movies")
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


if __name__ == "__main__":
    # Debug: Print the actual database path being used
    print(f"Database URL: {DB_URL}")
    db_file_path = os.path.join(project_root, 'data', 'movies.db')
    print(f"Database file path: {db_file_path}")
    print(f"File exists: {os.path.exists(db_file_path)}")
    print(f"File readable: {os.access(db_file_path, os.R_OK)}")
    print(f"File writable: {os.access(db_file_path, os.W_OK)}")

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