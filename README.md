# Movie App - SQL, API & HTML

## Overview
This project is a personal movie management application. 
It allows you to add, update, and delete movies, fetch movie details from an API, store data in a SQLite database, and generate a static website listing your movies.

## Features
- CRUD operations: Manage your movie collection from the CLI.
- Persistent storage: Uses SQLite for reliable data storage.
- API integration: Fetch movie posters and information automatically.
- Website generation: Generates an HTML page displaying all movies with posters and ratings.

## File Structure
movies_app_sql_api_html/
- storage/                 # Database storage scripts
- static/                  # CSS and placeholder images
- templates/               # HTML templates
- data/                    # SQLite database (currently in Git; will be removed later)
- movie_operations.py      # Core logic for CRUD
- movie_api.py             # API fetching logic
- website_generator.py     # HTML generation
- movies.html              # Generated website
- requirements.txt         # Dependencies
- README.md                # Project overview

## Setup
1. Clone the repository: `git clone <repo-url> && cd personal-movie-database`
2. Create a virtual environment and activate it: `python -m venv .venv && source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`

## Usage
Run your main application file: `python main.py`
Follow CLI prompts to add, update, delete, or list movies. Use `website_generator.py` to generate an HTML page of your movies.

## Contributing
- Currently, the SQLite database is included for testing. In the future, it will be excluded from Git.
- Please follow the existing code structure for new features or improvements.
