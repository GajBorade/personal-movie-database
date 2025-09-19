"""
Movie helper functions
"""

import sys
from colorama import Fore, Style
from movie_validators import get_valid_title, user_input_validity


def continue_or_quit():
    """Prompt user to continue or quit"""
    while True:
        user_choice = (
            input("\nPress 'enter' to continue or 'q' to exit: ")
            .strip().lower()
        )

        if user_choice in ["quit", "q"]:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "\nProgram closed successfully"
                + Style.RESET_ALL
            )
            sys.exit()
        elif user_choice == "":
            return
        else:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Invalid input. Press 'enter' or type 'q'."
                + Style.RESET_ALL
            )


def find_movie_for_update(movies_dict):
    """Find movie for updating"""
    user_input = get_valid_title()

    for title in movies_dict.keys():
        if title.lower() == user_input.lower():
            print(
                Fore.GREEN
                + Style.BRIGHT
                + f"\n{title} found in database"
                + Style.RESET_ALL
            )
            return title

    print(
        Fore.RED
        + Style.BRIGHT
        + f"\n{user_input} not found in database"
        + Style.RESET_ALL
    )
    return None


def get_user_confirmation(movie_title):
    """Get user confirmation for deletion"""
    while True:
        try:
            prompt = (
                input(f"\nDelete '{movie_title}'? Enter Yes/Y or No/N: ")
                .strip()
                .lower()
            )

            if not user_input_validity(prompt):
                continue

            if prompt in ["yes", "y"]:
                return True
            if prompt in ["no", "n"]:
                return False

            print(
                Fore.RED
                + Style.BRIGHT
                + "\nEnter either (Yes/Y or No/N)"
                + Style.RESET_ALL
            )
        except Exception as e:
            print(Fore.RED + Style.BRIGHT +
                  f"\nError occurred: {e}" +
                  Style.RESET_ALL
            )
            return False


def get_user_confirmation_for_update(movie_title):
    """Get user confirmation for what to update"""
    while True:
        try:
            prompt = (
                input(
                    f"\nWhat to update in '{movie_title}'?"
                    f"\nRating/R, Year/Y, or Both/B: "
                )
                .strip()
                .lower()
            )

            if not user_input_validity(prompt):
                continue

            if prompt in ["rating", "r"]:
                return "rating"
            if prompt in ["year", "y"]:
                return "year"
            if prompt in ["both", "b"]:
                return "both"

            print(
                Fore.RED
                + Style.BRIGHT
                + "\nEnter (Rating/R, Year/Y, or Both/B)"
                + Style.RESET_ALL
            )
        except Exception as e:
            print(Fore.RED + Style.BRIGHT +
                  f"\nError occurred: {e}" +
                  Style.RESET_ALL
            )
            return None


def exit_app():
    """Exit the application"""
    print(Fore.YELLOW + Style.BRIGHT + "\nBye!" + Style.RESET_ALL)
    sys.exit()


def welcome():
    """Welcome message"""
    print(
        Fore.MAGENTA
        + Style.BRIGHT
        + "********** My Movies Database **********"
        + Style.RESET_ALL
    )


def display_menu():
    """Display menu options"""
    print(
        Fore.CYAN + Style.BRIGHT + "\nMenu:\n"
        "0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
        "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
        "8. Movies sorted by rating\n9. Movies sorted by year"
        "\n10. Generate Website" + Style.RESET_ALL
    )


def get_user_choice():
    """Get valid user menu choice"""
    while True:
        display_menu()
        choice = input("\nEnter choice (0-10): ").strip()

        if choice.isdigit() and 0 <= int(choice) <= 10:
            return int(choice)

        print(
            Fore.RED
            + Style.BRIGHT
            + "Invalid input. Enter a number (0-10)."
            + Style.RESET_ALL
        )
