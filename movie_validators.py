"""
Movie validation functions
"""
import datetime
from colorama import Fore, Style

# Constants
MIN_YEAR = 1888
MAX_YEAR = datetime.datetime.now().year


def movie_title_validity(command_string):
    """Validates the movie title"""
    if not command_string:
        print(Fore.RED + Style.BRIGHT +
              "\nError: Movie name cannot be empty." +
              Style.RESET_ALL
        )
        return False

    if not any(char.isalnum() for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nTitles consisting symbols only are not allowed." +
              Style.RESET_ALL
        )
        return False

    return True


def year_validity(command_string):
    """Validates the release year input"""
    special_characters = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?\\")

    if not command_string:
        print(
            Fore.RED + Style.BRIGHT +
            f"\nError: Enter a 4-digit year between {MIN_YEAR} and {MAX_YEAR}." +
            Style.RESET_ALL
        )
        return False

    if any(char in special_characters for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nError: year cannot contain special characters." +
              Style.RESET_ALL
        )
        return False

    if not command_string.isdigit() or len(command_string) != 4:
        print(
            Fore.RED + Style.BRIGHT +
            f"\nError: Enter a 4-digit year between {MIN_YEAR} and {MAX_YEAR}." +
            Style.RESET_ALL
        )
        return False

    if not MIN_YEAR <= int(command_string) <= MAX_YEAR:
        print(Fore.RED + Style.BRIGHT +
              f"\nError: Year should be between {MIN_YEAR} and {MAX_YEAR}." +
              Style.RESET_ALL
        )
        return False

    return True


def ratings_validity(command_string):
    """Validates the ratings input"""
    special_characters = set("!@#$%^&*()_=+[]{}|;:'\",<>/?\\")

    if not command_string:
        print(Fore.RED + Style.BRIGHT +
              "\nEnter a value between 0-10 (e.g., 8.5)." +
              Style.RESET_ALL
        )
        return False

    if any(char in special_characters for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nError: ratings contains special characters." +
              Style.RESET_ALL
        )
        return False

    try:
        value = float(command_string)
        if 0 <= value <= 10:
            return True
        else:
            print(Fore.RED + Style.BRIGHT +
                  "\nInvalid range. Enter rating (0-10):" +
                  Style.RESET_ALL
            )
            return False
    except ValueError:
        print(Fore.RED + Style.BRIGHT +
              "\nInvalid input. Enter a float value (e.g., 8.5)." +
              Style.RESET_ALL
        )
        return False


def user_input_validity(command_string):
    """Validates simple yes/no user input"""
    special_characters = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?\\")

    if not command_string:
        print(Fore.RED + Style.BRIGHT +
              "\nInput cannot be empty. Enter (yes/no)." +
              Style.RESET_ALL
        )
        return False

    if not any(char.isalnum() for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nOnly symbols not allowed. Enter 'yes' or 'no'." +
              Style.RESET_ALL
        )
        return False

    if all(char.isdigit() for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nOnly digits not allowed. Enter 'yes' or 'no'." +
              Style.RESET_ALL
        )
        return False

    if any(char in special_characters for char in command_string):
        print(Fore.RED + Style.BRIGHT +
              "\nSpecial characters not allowed. Enter (Y/N)." +
              Style.RESET_ALL
        )
        return False

    return True


def get_valid_title():
    """Get valid movie title from user"""
    while True:
        user_input = input("\nEnter movie name: ").strip().title()
        if movie_title_validity(user_input):
            print(Fore.YELLOW + Style.BRIGHT +
                  f"\nMovie title {user_input} is valid." +
                  Style.RESET_ALL
            )
            return user_input


def get_valid_year_input():
    """Get valid year from user"""
    while True:
        user_input = input(f"Enter release year ({MIN_YEAR}-{MAX_YEAR}): ").strip()
        if year_validity(user_input):
            print(Fore.YELLOW + Style.BRIGHT +
                  f"\nYear {user_input} added successfully." +
                  Style.RESET_ALL
            )
            return int(user_input)


def get_valid_ratings():
    """Get valid rating from user"""
    while True:
        user_input = input("Enter movie rating (0-10): ").strip()
        if ratings_validity(user_input):
            print(Fore.YELLOW + Style.BRIGHT +
                  f"\nRating {user_input} is valid." +
                  Style.RESET_ALL
            )
            return round(float(user_input), 2)
