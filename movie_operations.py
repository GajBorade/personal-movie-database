"""
Core movie CRUD operations with API integration
"""

import random
import movie_storage_sql as storage
from colorama import Fore, Style
from titlecase import titlecase
from movie_validators import get_valid_title, get_valid_year_input, get_valid_ratings
from movie_helpers import (
    continue_or_quit,
    find_movie_for_update,
    get_user_confirmation,
    get_user_confirmation_for_update,
)
from movie_api import search_movie_api


def initialize_app_data():
    """Get movies data from database"""
    return storage.list_movies()


def list_movies(movies_dict):
    """List all movies"""
    if not movies_dict:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found. Add some movies first."
            + Style.RESET_ALL
        )
        continue_or_quit()
        return

    print(
        Fore.YELLOW
        + Style.BRIGHT
        + f"\n{len(movies_dict)} movies in total\n"
        + Style.RESET_ALL
    )

    title_width = max(len(title) for title in movies_dict.keys())
    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}"
        f"{'TITLE'.ljust(title_width)} | {'RATING'.center(6)} | YEAR"
        f"{Style.RESET_ALL}"
    )
    print(
        f"{Fore.WHITE}{Style.BRIGHT}"
        f"{'-' * title_width} |{'-' * 8}|-----"
        f"{Style.RESET_ALL}"
    )

    for title, details in movies_dict.items():
        rating, year = details["rating"], details["year"]
        if (
            isinstance(details, dict)
            and isinstance(rating, (int, float))
            and isinstance(year, int)
        ):
            print(
                f"{Fore.BLUE}{Style.BRIGHT}{titlecase(title).ljust(title_width)} |"
                f"{Fore.GREEN}{Style.BRIGHT}{str(f'{rating:.1f}').center(6)}  |"
                f"{Fore.GREEN}{Style.BRIGHT} {year}{Style.RESET_ALL}"
            )

    continue_or_quit()


def get_add_movie_choice():
    """Get user choice for how to add movie"""
    while True:
        try:
            choice = input(
                f"\n{Fore.CYAN}{Style.BRIGHT}"
                f"How would you like to add the movie?"
                f"{Style.RESET_ALL}\n"
                f"1. Search via API (automatic details)\n"
                f"2. Enter manually\n"
                f"Enter choice (1 or 2): "
            ).strip()

            if choice == "1":
                return "api"
            elif choice == "2":
                return "manual"
            else:
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    f"Invalid choice. Enter 1 or 2."
                    f"{Style.RESET_ALL}"
                )

        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Error: {e}{Style.RESET_ALL}")


def add_movie_via_api(movies_dict):
    """Add movie using API search"""
    api_result = search_movie_api()

    if api_result == "manual_entry":
        return add_movie_manually(movies_dict)

    if api_result:
        title, year, rating, poster_url = api_result

        # Check if movie already exists
        if title in movies_dict:
            print(
                f"{Fore.RED}{Style.BRIGHT}\n{title} "
                f"already exists in database"
                f"{Style.RESET_ALL}"
            )
            return False

        # Add to local dict and database
        movies_dict[title] = {"rating": rating, "year": year, "poster_url": poster_url}
        storage.add_movie(title, year, rating, poster_url)

        print(
            f"{Fore.GREEN}{Style.BRIGHT}\n{title} "
            f"successfully added via API!"
            f"{Style.RESET_ALL}"
        )
        return True

    return False


def add_movie_manually(movies_dict):
    """Add movie with manual input"""
    title = get_valid_title()

    if title in movies_dict:
        print(
            f"{Fore.RED}{Style.BRIGHT}\n{title} "
            f"already exists in database"
            f"{Style.RESET_ALL}"
        )
        return False

    rating = get_valid_ratings()
    year = get_valid_year_input()

    movies_dict[title] = {"rating": rating, "year": year}
    storage.add_movie(title, year, rating, "")

    print(
        f"{Fore.YELLOW}{Style.BRIGHT}\n{title}"
        f" successfully added manually!"
        f"{Style.RESET_ALL}"
    )
    return True


def add_movie(movies_dict):
    """
    Add a new movie - choose between API or manual
    with robust error handling
    """
    choice = get_add_movie_choice()

    success = False

    if choice == "api":
        print(
            f"\n{Fore.CYAN}{Style.BRIGHT}"
            f"Attempting to add movie via API..."
            f"{Style.RESET_ALL}"
        )
        success = add_movie_via_api(movies_dict)

        # If API method completely failed and user didn't switch to manual
        if not success:
            while True:
                retry_choice = input(
                    f"\n{Fore.YELLOW}API method unsuccessful."
                    f" Would you like to:{Style.RESET_ALL}\n"
                    f"1. Try API search again\n"
                    f"2. Switch to manual entry\n"
                    f"3. Return to main menu\n"
                    f"Enter choice (1-3): "
                ).strip()

                if retry_choice == "1":
                    print(
                        f"\n{Fore.CYAN}{Style.BRIGHT}"
                        f"Retrying API search..."
                        f"{Style.RESET_ALL}"
                    )
                    success = add_movie_via_api(movies_dict)
                    break
                elif retry_choice == "2":
                    print(
                        f"\n{Fore.CYAN}{Style.BRIGHT}"
                        f"Switching to manual entry..."
                        f"{Style.RESET_ALL}"
                    )
                    success = add_movie_manually(movies_dict)
                    break
                elif retry_choice == "3":
                    print(
                        f"\n{Fore.YELLOW}{Style.BRIGHT}"
                        f"Returning to main menu..."
                        f"{Style.RESET_ALL}"
                    )
                    break
                else:
                    print(
                        f"{Fore.RED}{Style.BRIGHT}"
                        f"Invalid choice. Please enter 1, 2, or 3."
                        f"{Style.RESET_ALL}"
                    )

    else:  # Manual entry
        print(
            f"\n{Fore.CYAN}{Style.BRIGHT}"
            f"Adding movie manually..."
            f"{Style.RESET_ALL}"
        )
        success = add_movie_manually(movies_dict)

        if not success:
            retry = (
                input(
                    f"\n{Fore.YELLOW}"
                    f"Would you like to try again? (y/n):"
                    f" {Style.RESET_ALL}"
                )
                .strip()
                .lower()
            )
            if retry in ["y", "yes"]:
                success = add_movie_manually(movies_dict)

    # Final status message
    if success:
        print(
            f"\n{Fore.GREEN}{Style.BRIGHT}"
            f"Movie successfully added to your database!"
            f"{Style.RESET_ALL}"
        )
    else:
        print(
            f"\n{Fore.YELLOW}{Style.BRIGHT}"
            f"No movie was added this time."
            f"{Style.RESET_ALL}"
        )

    continue_or_quit()


def delete_movie(movies_dict):
    """Delete a movie"""
    title = get_valid_title()

    found_title = None
    for t in movies_dict.keys():
        if t.lower() == title.lower():
            found_title = t
            break

    if found_title:
        print(
            Fore.GREEN
            + Style.BRIGHT
            + f"\n{found_title} found in database"
            + Style.RESET_ALL
        )

        if get_user_confirmation(title):
            movies_dict.pop(found_title)
            storage.delete_movie(found_title)
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + f"\n{title} successfully deleted"
                + Style.RESET_ALL
            )
        else:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + f"\n{title} was not deleted"
                + Style.RESET_ALL
            )
    else:
        print(
            Fore.RED
            + Style.BRIGHT
            + f"\n{title} not found in database"
            + Style.RESET_ALL
        )

    continue_or_quit()


def update_movie(movies_dict):
    """Update a movie"""
    title = find_movie_for_update(movies_dict)

    if not title:
        continue_or_quit()
        return

    choice = get_user_confirmation_for_update(title)

    if choice == "rating":
        rating = get_valid_ratings()
        movies_dict[title]["rating"] = rating
        storage.update_movie(title, movies_dict[title]["year"], rating)
        print(
            Fore.YELLOW + Style.BRIGHT + f"\n{title} rating updated" + Style.RESET_ALL
        )

    elif choice == "year":
        year = get_valid_year_input()
        movies_dict[title]["year"] = year
        storage.update_movie(title, year, movies_dict[title]["rating"])
        print(Fore.YELLOW + Style.BRIGHT + f"\n{title} year updated" + Style.RESET_ALL)

    elif choice == "both":
        rating = get_valid_ratings()
        year = get_valid_year_input()
        movies_dict[title]["rating"] = rating
        movies_dict[title]["year"] = year
        storage.update_movie(title, year, rating)
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + f"\n{title} rating & year updated"
            + Style.RESET_ALL
        )

    continue_or_quit()


def random_movie(movies_dict):
    """Get random movie recommendation"""
    if not movies_dict:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found. Add some movies first."
            + Style.RESET_ALL
        )
    else:
        title, details = random.choice(list(movies_dict.items()))
        print(
            f"\n{Fore.BLUE}{Style.BRIGHT}Your movie for tonight: "
            f"{Fore.GREEN}{Style.BRIGHT}{title}, "
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"rated {Fore.GREEN}{Style.BRIGHT}{details['rating']} "
            f"{Fore.BLUE}{Style.BRIGHT}"
            f"from {Fore.GREEN}{Style.BRIGHT}"
            f"{details['year']}"
            f"{Style.RESET_ALL}"
        )

    continue_or_quit()


def search_movie(movies_dict):
    """Search for movies"""
    search_term = input("\nEnter part of movie name: ").strip().lower()
    matches = [
        (title, details)
        for title, details in movies_dict.items()
        if search_term in title.lower()
    ]

    if not matches:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found matching your search"
            + Style.RESET_ALL
        )
    else:
        for title, details in matches:
            print(
                f"{Fore.BLUE}{Style.BRIGHT}{title}{Style.RESET_ALL}, "
                f"{Fore.GREEN}{Style.BRIGHT}"
                f"Rating: {details['rating']:.1f}, "
                f"Year: {details['year']}{Style.RESET_ALL}"
            )

    continue_or_quit()
