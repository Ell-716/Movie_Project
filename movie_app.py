import statistics
import os
import requests
import random
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from colorama import init, Fore
from fuzzywuzzy import process

load_dotenv()
API_KEY = os.getenv("API_KEY")


class MovieApp:
    """
    The MovieApp class provides the main interface for interacting with a movie storage system.
    It allows users to fetch movie data from the OMDb API, store movies, and retrieve information
    using a given storage backend. The class initializes with the specified storage and loads
    existing movies upon startup.
    Attributes:
        _storage (IStorage): The storage instance to manage movie data.
        _movies (dict): A dictionary of movies retrieved from the storage.
    """

    def __init__(self, storage):
        """
        Initialize the MovieApp instance with specified storage.
        Args:
            storage (IStorage): An instance of a storage class implementing the IStorage interface.
        """
        init(autoreset=True)
        self._storage = storage
        self._movies = self._storage.list_movies()

    @staticmethod
    def _fetch_movie_data(title):
        """
        Fetch detailed movie data from the OMDb API by title.
        Args:
            title (str): The title of the movie to fetch from the API.
        Returns:
            dict or None: A dictionary of movie details (e.g., Title, Year, Rating, Poster) if successful,
                          or None if an error occurs or the movie is not found.
        """
        api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

            data = response.json()
            if "Error" in data:
                print(Fore.RED + f"Error fetching movie data: {data['Error']}")
                return None

            return data

        except (HTTPError, ConnectionError, Timeout) as req_err:
            print(Fore.RED + f"Request error occurred: {req_err}")
        except ValueError as json_err:
            print(Fore.RED + f"Error parsing JSON: {json_err}")
        except RequestException as err:
            print(Fore.RED + f"An unexpected error occurred: {err}")

        return None

    def _is_movie_list_empty(self):
        """
        Checks if the movie list is empty and prints a message.
        Returns:
            bool: True if the movie list is empty, False otherwise.
        """
        if len(self._movies) == 0:
            print(Fore.RED + "There are no movies available.")
            return True
        return False

    @staticmethod
    def _valid_movie_name():
        """
        Prompts the user for a valid movie name.
        Returns:
            str: The movie name entered by the user.
        """
        while True:
            movie_name = input("Enter movie name: ").strip()
            if movie_name == "":
                print(Fore.RED + "Movie name cannot be empty.")
            else:
                return movie_name

    @staticmethod
    def _valid_rating():
        """
        Prompts the user for a valid rating between 0 and 10.
        Returns:
            float: The rating entered by the user.
        """
        while True:
            try:
                rating = float(input("Enter new movie rating (0-10): "))
                if 0 <= rating <= 10:
                    return rating
                else:
                    print(Fore.RED + "Please enter a rating between 0 and 10.")
            except ValueError:
                print(Fore.RED + "Please enter a valid rating.")

    def _command_list_movies(self):
        """
        Displays the total number of movies and a list of each movie
        with its year and rating.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        print(Fore.MAGENTA + f"{len(self._movies)} movies in total")
        for movie_title, details in self._movies.items():
            print(f"{movie_title} ({details['Year']}), {details['Rating']}, {details['Poster']}")

    def _command_add(self):
        """
        Adds a new movie to the storage if it doesn't already exist. Prompts the user to enter
        the movie name, release year, and rating, and then saves the new movie to storage.
        Returns:
            None
        """
        movie_name = self._valid_movie_name()
        data = self._fetch_movie_data(movie_name)

        if data is None:
            return

        if movie_name in self._movies:
            print(Fore.RED + f"Movie '{movie_name}' already exists!")
            return

        # Extract data safely
        title = data.get("Title")
        year = int(data.get("Year")) if data.get("Year") else None
        rating = float(data.get("imdbRating")) if data.get("imdbRating") else None
        poster = data.get("Poster")

        if title and year is not None and rating is not None and poster:
            self._storage.add_movie(title, year, rating, poster)
            print(Fore.GREEN + f"Movie '{title}' successfully added!")
            self._movies = self._storage.list_movies()
        else:
            print(Fore.RED + "Some details are missing in the movie data. Please try another movie.")

    def _command_delete(self):
        """
        Removes a movie from the storage if it exists.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        # Get the movie name from the user and normalize it for case-insensitive comparison
        movie_to_delete = self._valid_movie_name()
        normalized_movies = {title.lower(): title for title in self._movies}

        if movie_to_delete in normalized_movies:
            original_name = normalized_movies[movie_to_delete]
            try:
                self._storage.delete_movie(original_name)
                print(Fore.GREEN + f"Movie '{original_name}' successfully deleted.")
                self._movies = self._storage.list_movies()
            except Exception as e:
                print(Fore.RED + f"Failed to delete movie '{original_name}': {e}")
        else:
            print(Fore.RED + f"Movie '{movie_to_delete}' doesn't exist!")

    def _command_update(self):
        """
        Updates the rating of an existing movie in the storage if it exists.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        # Get the movie name from the user and normalize it for case-insensitive comparison
        movie_to_update = self._valid_movie_name().strip().lower()
        normalized_movies = {name.lower(): name for name in self._movies}

        # Check if the movie exists in the normalized dictionary
        if movie_to_update in normalized_movies:
            original_name = normalized_movies[movie_to_update]
            rating = self._valid_rating()

            # Try to update the movie rating in storage
            try:
                self._storage.update_movie(original_name, rating)
                print(Fore.GREEN + f"Movie '{original_name}' successfully updated.")
                self._movies = self._storage.list_movies()
            except Exception as e:
                print(Fore.RED + f"Failed to update movie '{original_name}': {e}")
        else:
            print(Fore.RED + f"Movie '{movie_to_update}' doesn't exist!")

    def _command_statistics(self):
        """
        Displays statistical information about the movies' ratings in `self._movies`.
        This function calculates and prints:
        - The average rating of all movies.
        - The median rating of all movies.
        - The best movies (with the highest rating).
        - The worst movies (with the lowest rating).
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        ratings = [details["Rating"] for details in self._movies.values()]

        # Calculate and display average rating
        average = sum(ratings) / len(ratings)
        print(f"Average rating: {average:.1f}")

        # Calculate and display median rating
        try:
            median = statistics.median(ratings)
            print(f"Median rating: {median:.1f}")
        except statistics.StatisticsError:
            print(Fore.RED + "Error calculating median rating.")
            return

        # Display best movies (highest rating)
        self._print_movies_with_rating("Best", max(ratings))

        # Display worst movies (lowest rating)
        self._print_movies_with_rating("Worst", min(ratings))

    def _print_movies_with_rating(self, descriptor, rating):
        """
        Helper method to print movies with a specific rating.
        Args:
            descriptor (str): Descriptor to label the movies (e.g., "Best" or "Worst").
            rating (float): The rating to filter and display movies by.
        Returns:
            None
        """
        movies_with_rating = [movie for movie, details in self._movies.items() if details["Rating"] == rating]
        for movie in movies_with_rating:
            print(f"{descriptor} movie: {movie}: {self._movies[movie]['Rating']}")

    def _command_random_movie(self):
        """
        Selects and displays a random movie from the movies storage along with its rating.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        random_film = random.choice(list(self._movies.keys()))
        print(f"Your movie for tonight: {random_film}, it's rated {self._movies[random_film]['Rating']}")

    def _command_search(self):
        """
        Searches for movies based on a partial name input using fuzzy string matching.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        part_of_name = input("Enter part of movie name: ").lower()

        # Check for a short input string
        if len(part_of_name) < 2:  # Minimum length for search
            print(Fore.RED + "Please enter at least 2 characters for the search.")
            return

        movie_titles = list(self._movies.keys())

        # Use fuzzy matching to find close matches
        matches = process.extract(part_of_name, movie_titles, limit=5)

        # Filter matches based on a similarity threshold
        threshold = 60
        similar_movies = [match for match, score in matches if score > threshold]

        if similar_movies:
            print(f"The movie \"{part_of_name}\" does not exist. Did you mean:")
            for movie in similar_movies:
                print(f"{movie}: {self._movies[movie]['Rating']}")
        else:
            print(Fore.RED + "No similar movies found.")

    def _sorted_by_rating(self):
        """
        Prints the movies sorted by their ratings in descending order.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        sorted_movies = sorted(self._movies.items(), key=lambda item: item[1]["Rating"], reverse=True)
        for movie, details in sorted_movies:
            print(f"{movie} ({details['Year']}): {details['Rating']:.1f}")

    def _sorted_by_year(self):
        """
        Sorts and displays movies in chronological order based on their release year.
        Returns:
            None
        """
        if self._is_movie_list_empty():
            return

        while True:
            # Prompt the user to choose sorting order
            latest_movies = input("Do you want the latest movies first? (Y/N): ").strip().lower()
            print()

            if latest_movies == "y":
                # Sort movies by year, latest movies first
                latest_first = sorted(self._movies.items(), key=lambda item: item[1]["Year"], reverse=True)
                for movie, details in latest_first:
                    print(
                        f"{movie} ({details['Year']}): {details['Rating']:.1f}")
                break

            elif latest_movies == "n":
                # Sort movies by year, oldest movies first
                latest_last = sorted(self._movies.items(), key=lambda item: item[1]["Year"])
                for movie, details in latest_last:
                    print(
                        f"{movie} ({details['Year']}): {details['Rating']:.1f}")
                break

            else:
                print("Please enter 'Y' or 'N'")
                continue

    def _filter_movies(self):
        """
        Filters movies based on the user's input for minimum rating, start year, and end year.
        Returns:
            None
        """
        # Check if the movie list is empty
        if self._is_movie_list_empty():
            return

        # Prompt user for minimum rating (allow blank input)
        while True:
            min_rating = input("Enter minimum rating (leave blank for no minimum rating): ")
            if min_rating == "":
                min_rating = None
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
                start_year = None
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
            end_year = input("Enter end year (leave blank for no end year): \n")
            if end_year == "":
                end_year = None
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
        for movie, details in self._movies.items():
            year = details['Year']
            rating = details['Rating']

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

    def _generate_website(self):
        ...

    def run(self):
        """
        Run function to run the Movies Database application.

        This function displays a menu to the user and handles user input to perform various operations,
        such as listing movies, adding/deleting movies, updating ratings, displaying statistics,
        selecting a random movie, searching for a movie, and sorting movies by rating.
        The program runs in a loop until the user chooses to exit.
        Returns:
            None
        Raises:
            ValueError: If the user input is not a valid integer choice from the menu.
        """
        print(Fore.CYAN + "\n********** My Movies Database **********")

        while True:
            try:
                # Display the menu
                print("\nMenu:")
                for key, (description, _) in self.menu.items():
                    print(f"{key}. {description}")

                choice = int(input(Fore.YELLOW + "\nEnter choice (0-11): "))
                print()

                # Handle the user's menu choice
                if choice in self.menu:
                    function = self.menu[choice][1]
                    if function is not None:
                        function(self)
                    else:
                        print("Bye!")
                        break
                else:
                    print(Fore.RED + "Invalid choice. Please enter a number between 0 and 11.")
            except ValueError:
                print(Fore.RED + "Invalid choice. Please enter a number between 0 and 11.")
            print()
            input(Fore.BLUE + "Press enter to continue")

    # Define the menu options and corresponding functions
    menu = {
        0: ("Exit", None),
        1: ("List movies", _command_list_movies),
        2: ("Add movie", _command_add),
        3: ("Delete movie", _command_delete),
        4: ("Update movie", _command_update),
        5: ("Stats", _command_statistics),
        6: ("Random movie", _command_random_movie),
        7: ("Search movie", _command_search),
        8: ("Movies sorted by rating", _sorted_by_rating),
        9: ("Movies sorted by year", _sorted_by_year),
        10: ("Filter movies", _filter_movies),
        11: ("Generate website", _generate_website)
    }
