"""
Movie statistics and sorting functions
"""

from colorama import Fore, Style
from movie_helpers import continue_or_quit


def calculate_average_and_median(movies_dict):
    """Calculate and display average and median ratings"""
    ratings = [details["rating"] for details in movies_dict.values()]
    total_movies = len(ratings)
    average = sum(ratings) / total_movies

    print(
        f"\n{Fore.BLUE}{Style.BRIGHT}"
        f"Average rating:"
        f" {Fore.GREEN}{Style.BRIGHT}{average:.1f}"
        f"{Style.RESET_ALL}"
    )

    # Median calculation
    sorted_ratings = sorted(ratings)
    middle = total_movies // 2

    if total_movies % 2 != 0:
        median = sorted_ratings[middle]
    else:
        median = (sorted_ratings[middle] + sorted_ratings[middle - 1]) / 2

    print(
        f"{Fore.BLUE}{Style.BRIGHT}"
        f"Median rating:"
        f" {Fore.GREEN}{Style.BRIGHT}{median:.1f}"
        f"{Style.RESET_ALL}"
    )


def best_and_worst_movies(movies_dict):
    """Display best and worst movies"""
    ratings = [(title, details["rating"]) for title, details in movies_dict.items()]
    max_rating = max(ratings, key=lambda x: x[1])[1]
    min_rating = min(ratings, key=lambda x: x[1])[1]

    best_movies = [movie for movie in ratings if movie[1] == max_rating]
    worst_movies = [movie for movie in ratings if movie[1] == min_rating]

    print(f"\n{Fore.BLUE}{Style.BRIGHT}"
          f"🎬 Best movie(s):"
          f"{Style.RESET_ALL}"
    )
    for title, rating in best_movies:
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}"
            f"-> {title} - {Fore.GREEN}{Style.BRIGHT}"
            f"{rating:.1f}"
            f"{Style.RESET_ALL}"
        )

    print(f"\n{Fore.BLUE}{Style.BRIGHT}"
          f"🎬 Worst movie(s):"
          f"{Style.RESET_ALL}"
    )
    for title, rating in worst_movies:
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}"
            f"-> {title} - {Fore.GREEN}{Style.BRIGHT}"
            f"{rating:.1f}"
            f"{Style.RESET_ALL}"
        )


def stats(movies_dict):
    """Display movie statistics"""
    if not movies_dict:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found. Add some movies first."
            + Style.RESET_ALL
        )
        continue_or_quit()
        return

    calculate_average_and_median(movies_dict)
    best_and_worst_movies(movies_dict)
    continue_or_quit()


def movies_sorted_by_rating(movies_dict):
    """Display movies sorted by rating"""
    if not movies_dict:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found. Add some movies first."
            + Style.RESET_ALL
        )
        continue_or_quit()
        return

    sorted_movies = sorted(movies_dict.items(), key=lambda x: (-x[1]["rating"], x[0]))

    print(
        f"\n{Fore.YELLOW}{Style.BRIGHT}"
        f"⭐ Movies Sorted by Rating (Highest to Lowest):\n"
        f"{Style.RESET_ALL}"
    )

    for title, details in sorted_movies:
        print(
            f"{Fore.BLUE}{title}{Style.RESET_ALL}, "
            f"{Fore.MAGENTA}{Style.BRIGHT}Rating:"
            f" {details['rating']:.1f},{Style.RESET_ALL} "
            f"{Fore.GREEN}Year: {details['year']}"
            f"{Style.RESET_ALL}"
        )

    continue_or_quit()


def movies_sorted_by_year(movies_dict):
    """Display movies sorted by year"""
    if not movies_dict:
        print(
            Fore.RED
            + Style.BRIGHT
            + "No movies found. Add some movies first."
            + Style.RESET_ALL
        )
        continue_or_quit()
        return

    sorted_movies = sorted(movies_dict.items(), key=lambda x: (-x[1]["year"], x[0]))

    print(
        f"\n{Fore.YELLOW}{Style.BRIGHT}"
        f"🎬 Movies Sorted by Year (Newest to Oldest):\n"
        f"{Style.RESET_ALL}"
    )

    for title, details in sorted_movies:
        print(
            f"{Fore.BLUE}{title}{Style.RESET_ALL}, "
            f"{Fore.GREEN}Rating: {details['rating']:.1f},{Style.RESET_ALL} "
            f"{Fore.MAGENTA}{Style.BRIGHT}Year: {details['year']}"
            f"{Style.RESET_ALL}"
        )

    continue_or_quit()
