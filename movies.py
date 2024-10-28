from storage_json import StorageJson
import statistics
import random
from colorama import init, Fore
from fuzzywuzzy import process

# Import all functions from the specified modules
init(autoreset=True)  # Initialize colorama

# Load movies from the JSON file
storage = StorageJson('data.json')
movies = storage.list_movies()


def is_movie_list_empty(movies):
    """Checks if the movie list is empty and prints a message."""
    if len(movies) == 0:
        print(Fore.RED + "There are no movies available.")
        return True
    return False


def get_valid_movie_name():
    """Prompts the user for a valid movie name."""
    while True:
        movie_name = input("Enter movie name: ").strip()
        if movie_name == "":
            print(Fore.RED + "Movie name cannot be empty.")
        return movie_name


def get_valid_rating():
    """Prompts the user for a valid rating between 0 and 10."""
    while True:
        try:
            rating = float(input("Enter new movie rating (0-10): "))
            if 0 <= rating <= 10:
                return rating
            else:
                print(Fore.RED + "Please enter a rating between 0 and 10.")
        except ValueError:
            print(Fore.RED + "Please enter a valid rating.")


def movies_and_rating(movies):
    """
    Displays the total number of movies and a list of each movie
    with its year and rating.
    If no movies are available, it informs the user that there are
    no movies to display.
    Args:
    movies (dict): A dictionary containing movie titles as keys,
    and a dictionary with 'rating' and 'year' as values.
    """
    if is_movie_list_empty(movies):
        return

    print(Fore.MAGENTA + f"{len(movies)} movies in total")
    for movie, details in movies.items():
        print(f"{movie} ({details['year']}): {details['rating']:.1f}")


def adding_new_movie(movies):
    """
    Adds a new movie to the movies dictionary with its year and rating.
    The user is prompted to input the movie's name, year, and rating.
    If the movie already exists, a message is displayed.
    """
    movie_name = get_valid_movie_name()
    if movie_name.lower() in [name.lower() for name in movies]:
        print(Fore.RED + f"Movie '{movie_name}' already exists!")
        return

    # Ask for the release year and ensure it's valid
    while True:
        try:
            year = int(input("Enter the release year of the movie: "))
            break  # Break the loop if a valid year is entered
        except ValueError:
            print(Fore.RED + "Please enter a valid year.")

    rating = get_valid_rating()
    poster = None
    storage.add_movie(movie_name, year, rating, poster)
    print(Fore.GREEN + f"Movie '{movie_name}' successfully added!")


def removing_movie(movies):
    """
    Removes a movie from the movies dictionary if it exists.
    The user is prompted to input the movie's name.
    The function checks for empty input and whether the movie exists in the dictionary.
    If the movie is found, it is deleted, and a confirmation message is shown.
    If the movie is not found or if no movies exist, an appropriate message is displayed.
    """
    if is_movie_list_empty(movies):
        return

    movie_to_delete = get_valid_movie_name().strip().lower()

    # Create a normalized dictionary for case-insensitive matching
    normalized_movies = {name.lower(): name for name in movies}

    if movie_to_delete in normalized_movies:
        original_name = normalized_movies[movie_to_delete]
        storage.delete_movie(original_name)
        print(Fore.GREEN + f"Movie '{original_name}' successfully deleted.")
    else:
        print(Fore.RED + f"Movie '{movie_to_delete}' doesn't exist!")


def update_rating(movies):
    """
    Updates the rating of an existing movie in the movies' dictionary.
    The user is prompted to input the movie's name and the new rating. If the movie
    exists in the dictionary, the rating is updated and a confirmation message is shown.
    If the movie is not found, an error message is displayed.
    """
    if is_movie_list_empty(movies):
        return

    movie_to_update = get_valid_movie_name().strip().lower()

    # Create a normalized dictionary for case-insensitive matching
    normalized_movies = {name.lower(): name for name in movies}

    if movie_to_update in normalized_movies:
        original_name = normalized_movies[movie_to_update]  # Get original case name
        rating = get_valid_rating()
        storage.update_movie(original_name, rating)
        print(Fore.GREEN + f"Movie '{movie_to_update}' successfully updated.")
    else:
        print(Fore.RED + f"Movie '{movie_to_update}' doesn't exist!")


def movie_statistics(movies):
    """
    Displays statistical information about the movies' ratings.
    This function calculates and prints:
    - The average rating of all movies.
    - The median rating of all movies.
    - The best movies (with the highest rating).
    - The worst movies (with the lowest rating).
    """
    if is_movie_list_empty(movies):
        return

    ratings = [details["rating"] for details in movies.values()]
    average = sum(ratings) / len(ratings)
    median = statistics.median(ratings)

    print(f"Average rating: {average:.1f}")
    print(f"Median rating: {median:.1f}")

    max_rating = max(ratings)
    best_movies = [movie for movie, details in movies.items() if details["rating"] == max_rating]
    for movie in best_movies:
        print(f"Best movie: {movie}: {movies[movie]['rating']}")

    min_rating = min(ratings)
    worst_movies = [movie for movie, details in movies.items() if details["rating"] == min_rating]
    for movie in worst_movies:
        print(f"Worst movie: {movie}: {movies[movie]['rating']}")


def random_movie_rating(movies):
    """
    Selects and displays a random movie from the movies dictionary along with its rating.
    This function randomly picks a movie from the dictionary and prints its title and rating.
    """
    if is_movie_list_empty(movies):
        return

    random_film = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {random_film}, it's rated {movies[random_film]['rating']}")


def search_movie(movies):
    """
    Searches for movies based on a partial name input using fuzzy string matching.
    If no exact match is found, suggests similar movie titles.
    """
    if is_movie_list_empty(movies):
        return

    part_of_name = input("Enter part of movie name: ").lower()
    movie_titles = list(movies.keys())

    # Use fuzzy matching to find close matches
    matches = process.extract(part_of_name, movie_titles, limit=5)

    # Filter matches based on a similarity threshold
    threshold = 60
    similar_movies = [match for match, score in matches if score > threshold]

    if similar_movies:
        print(f"The movie \"{part_of_name}\" does not exist. Did you mean:")
        for movie in similar_movies:
            print(f"{movie}: {movies[movie]['rating']}")
    else:
        print(Fore.RED + "No similar movies found.")


def sorted_by_rating(movies):
    """
    Prints the movies sorted by their ratings in descending order.
    The function sorts the movies dictionary by ratings, with the highest rating first,
    and prints each movie title along with its rating.
    """
    if is_movie_list_empty(movies):
        return

    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
    for movie, details in sorted_movies:
        print(f"{movie} ({details['year']}): {details['rating']}")


def sorted_by_year(movies):
    """
    Sorts and displays movies in chronological order based on their release year.
    The user is asked if they want the latest movies first or last, and the function
    sorts the movies accordingly and displays them with their year and rating.
    Args:
    movies (dict): A dictionary of movie titles and their associated information (year and rating).
    """

    if is_movie_list_empty(movies):
        return

    while True:
        # Prompt the user to choose sorting order
        latest_movies = input("Do you want the latest movies first? (Y/N): ").strip().lower()
        print()

        # Check if the input is valid
        if latest_movies == "y":
            # Sort movies by year, latest movies first
            latest_first = sorted(movies.items(), key=lambda item: item[1]["year"], reverse=True)
            for movie, details in latest_first:
                print(f"{movie} ({details['year']}): {details['rating']}")
            break  # Exit the loop after displaying the list

        elif latest_movies == "n":
            # Sort movies by year, oldest movies first
            latest_last = sorted(movies.items(), key=lambda item: item[1]["year"])
            for movie, details in latest_last:
                print(f"{movie} ({details['year']}): {details['rating']}")
            break  # Exit the loop after displaying the list

        else:
            # If the input is invalid, ask the user to enter a valid choice
            print("Please enter 'Y' or 'N'")
            continue  # Continue prompting the user for valid input


def filter_movies(movies):
    """
    Filters movies based on the user's input for minimum rating, start year, and end year.
    The user can leave inputs blank to apply no filter for a particular criterion.
    The filtered list of movies is displayed with their titles, release years, and ratings.
    """

    if is_movie_list_empty(movies):
        return

    # Prompt user for minimum rating (allow blank input)
    while True:
        min_rating = input("Enter minimum rating (leave blank for no minimum rating): ")
        if min_rating == "":
            min_rating = None  # No minimum rating
            break
        try:
            min_rating = float(min_rating)
            if 0 <= min_rating <= 10:
                break
            else:
                print(Fore.RED + "Please enter a rating between 0 and 10.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid rating.")

    # Prompt user for start year (allow blank input)
    while True:
        start_year = input("Enter start year (leave blank for no start year): ")
        if start_year == "":
            start_year = None  # No start year filter
            break
        try:
            start_year = int(start_year)
            if 1888 <= start_year <= 2024:
                break
            else:
                print(Fore.RED + "Please enter a year between 1888 and 2024.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid year.")

    # Prompt user for end year (allow blank input)
    while True:
        end_year = input("Enter end year (leave blank for no end year): ")
        if end_year == "":
            end_year = None  # No end year filter
            break
        try:
            end_year = int(end_year)
            if 1888 <= end_year <= 2024:
                break
            else:
                print(Fore.RED + "Please enter a year between 1888 and 2024.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid year.")

    # Apply the filtering logic
    filtered_movies = []
    for movie, details in movies.items():
        year = details['year']
        rating = details['rating']

        # Filter based on user inputs
        if (min_rating is None or rating >= min_rating) and \
           (start_year is None or year >= start_year) and \
           (end_year is None or year <= end_year):
            filtered_movies.append((movie, year, rating))

    # Display the filtered movies
    if filtered_movies:
        for movie, year, rating in filtered_movies:
            print(f"{movie} ({year}): {rating}")
    else:
        print(Fore.RED + "No movies match the filter criteria.")


def main():
    """
    Main function to run the Movies Database application.
    Displays a menu to the user and handles user input to perform different operations
    such as listing movies, adding/deleting movies, updating ratings, displaying statistics,
    selecting a random movie, searching for a movie, and sorting movies by rating.
    The program runs in a loop until the user chooses to exit.
    """
    print(Fore.CYAN + "********** My Movies Database **********")
    while True:
        try:
            print(Fore.GREEN + MENU)
            choice = int(input(Fore.YELLOW + "Enter choice (0-9): "))
            print()

            # Reload movies to ensure the latest data is used
            movies = storage.list_movies()

            # Handle the user's menu choice
            if choice == 1:
                movies_and_rating(movies)
            elif choice == 2:
                adding_new_movie(movies)
            elif choice == 3:
                removing_movie(movies)
            elif choice == 4:
                update_rating(movies)
            elif choice == 5:
                movie_statistics(movies)
            elif choice == 6:
                random_movie_rating(movies)
            elif choice == 7:
                search_movie(movies)
            elif choice == 8:
                sorted_by_rating(movies)
            elif choice == 9:
                sorted_by_year(movies)
            elif choice == 10:
                filter_movies(movies)
            elif choice == 0:
                print("Bye!")
                break  # Exit the program
            elif choice < 0 or choice > 9:
                print(Fore.RED + "Invalid choice. Please enter a number between 0 and 9.")
        except ValueError:
            print(Fore.RED + "Invalid choice. Please enter a number between 0 and 9.")
        print()
        input(Fore.BLUE + "Press enter to continue")


# The menu options to be displayed to the user
MENU = """
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Movies sorted by year
10. Filter movies
"""


if __name__ == "__main__":
    main()
