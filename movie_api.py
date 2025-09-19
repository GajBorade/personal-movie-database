"""
Movie API integration with OMDb API
"""

import requests
from colorama import Fore, Style

API_KEY = "ca5c32f4"
REQUEST_URL = "http://www.omdbapi.com/"


def get_movie_from_api(search_title):
    """
    Requests movie details from the OMDb API based on movie title.

    Parameters:
        search_title (str): Movie title to search for

    Returns:
        tuple: (Title, Year, imdbRating, Poster) or None if not found
    """
    parameter = {"t": search_title, "apikey": API_KEY}

    try:
        res = requests.get(REQUEST_URL, params=parameter)
        res.raise_for_status()
        data = res.json()

        if data.get("Response") == "True":
            # Extract data
            title = data.get("Title")
            year = int(data.get("Year", 0))
            rating = (
                float(data.get("imdbRating", 0.0))
                if data.get("imdbRating") not in ["N/A", None]
                else 0.0
            )
            poster_url = data.get("Poster", "")

            return title, year, rating, poster_url
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                f"Movie '{search_title}' not found: "
                f"{data.get('Error')}{Style.RESET_ALL}"
            )
            return None

    except requests.exceptions.HTTPError as e:
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"Error accessing the API: {e}"
            f"{Style.RESET_ALL}"
        )
        return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{Style.BRIGHT}" f"Network error: {e}" f"{Style.RESET_ALL}")
        return None
    except ValueError as e:
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"Error parsing API response: {e}"
            f"{Style.RESET_ALL}"
        )
        return None


def search_movie_api():
    """
    Interactive function to search for movie via API with comprehensive
    error handling

    Returns:
        tuple: (Title, Year, imdbRating, Poster) or None if not found/error
    """
    # Input validation
    while True:
        search_title = input("Enter movie title to search: ").strip()

        if not search_title:
            print(
                f"{Fore.RED}{Style.BRIGHT}Movie title cannot be empty. "
                f"Please try again.{Style.RESET_ALL}"
            )
            continue
        elif len(search_title) < 2:
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}Title too short. "
                f"Please enter at least 2 characters.{Style.RESET_ALL}"
            )
            continue
        else:
            break

    print(
        f"{Fore.YELLOW}{Style.BRIGHT}Searching for '{search_title}' "
        f"in OMDb database...{Style.RESET_ALL}"
    )

    # Attempt API call
    result = get_movie_from_api(search_title)

    # Handle different result scenarios
    if result is None:
        print(
            f"\n{Fore.RED}{Style.BRIGHT} "
            f"Unable to fetch movie data from API"
            f"{Style.RESET_ALL}"
        )

        # Offer options when API fails
        while True:
            choice = input(
                f"\n{Fore.CYAN}What would you like to do?"
                f"{Style.RESET_ALL}\n"
                f"1. Try searching for a different movie\n"
                f"2. Enter movie details manually\n"
                f"3. Return to main menu\n"
                f"Enter choice (1-3): "
            ).strip()

            if choice == "1":
                return search_movie_api()  # Recursive call to try again
            elif choice == "2":
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    f"Switching to manual entry mode..."
                    f"{Style.RESET_ALL}"
                )
                return "manual_entry"  # Signal to switch to manual mode
            elif choice == "3":
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    f"Returning to main menu..."
                    f"{Style.RESET_ALL}"
                )
                return None
            else:
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    f"Invalid choice. Please enter 1, 2, or 3."
                    f"{Style.RESET_ALL}"
                )

    else:
        title, year, rating, poster_url = result

        # Display found movie details
        print(f"\n{Fore.GREEN}{Style.BRIGHT}" f"Found movie:" f"{Style.RESET_ALL}")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"Title: "
            f"{Fore.WHITE}{title}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"Year: "
            f"{Fore.WHITE}{year}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"IMDB Rating: {Fore.WHITE}{rating}/10"
            f"{Style.RESET_ALL}"
        )
        print(
            f"{Fore.BLUE}{Style.BRIGHT}Poster: "
            f"{Fore.WHITE}{'Available' if poster_url else 'Not available'}"
            f"{Style.RESET_ALL}"
        )

        # Validate data quality
        data_warnings = []
        if year == 0:
            data_warnings.append("Year information missing")
        if rating == 0.0:
            data_warnings.append("Rating information missing")
        if not poster_url:
            data_warnings.append("Poster not available")

        if data_warnings:
            print(
                f"\n{Fore.YELLOW}{Style.BRIGHT}"
                f"Data Quality Warnings:{Style.RESET_ALL}"
            )
            for warning in data_warnings:
                print(f"{Fore.YELLOW}{warning}{Style.RESET_ALL}")

        # Get user confirmation
        while True:
            confirm = (
                input(
                    f"\n{Fore.CYAN}Add this movie to your database? (y/n): "
                    f"{Style.RESET_ALL}"
                )
                .strip()
                .lower()
            )

            if confirm in ["y", "yes"]:
                return result
            elif confirm in ["n", "no"]:
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    f"Movie not added. Returning to menu..."
                    f"{Style.RESET_ALL}"
                )
                return None
            else:
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    f"Please enter 'y' for yes or 'n' for no."
                    f"{Style.RESET_ALL}"
                )


def test_api_connection():
    """
    Test if API is accessible - useful for debugging

    Returns:
        bool: True if API is accessible, False otherwise
    """
    try:
        test_params = {"t": "test", "apikey": API_KEY}
        response = requests.get(REQUEST_URL, params=test_params, timeout=5)
        return response.status_code == 200
    except requests.exceptions.HTTPError as e:
        print(f"Error accessing the API request: {e}")
        return False
