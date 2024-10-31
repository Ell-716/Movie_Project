from abc import ABC, abstractmethod
from colorama import init, Fore

init(autoreset=True)


class IStorage(ABC):
    """
    IStorage is an abstract base class that defines the interface for
    storage operations related to movie data.
    This class provides methods for listing, saving, adding, deleting,
    and updating movie entries, serving as a template for specific storage
    implementations (e.g., JSON or CSV storage). Each method manipulates
    a movie dictionary where the movie title is a key, and the value is a
    dictionary of movie details.
    Methods:
        list_movies(): Retrieves a dictionary of movies from storage.
        save_movies(movies): Saves a dictionary of movies to storage.
        add_movie(title, year, rating, poster): Adds a new movie to storage.
        delete_movie(title): Deletes a movie by title from storage.
        update_movie(title, rating): Updates the rating of an existing movie.
    """

    @abstractmethod
    def list_movies(self):
        """
        Retrieve a dictionary of movies from the storage.
        Returns:
            dict: A dictionary where each key is a movie title, and each
                  value is a dictionary of details (Year, Rating, Poster).
        """
        pass

    @abstractmethod
    def save_movies(self, movies):
        """
        Save the provided dictionary of movies to the storage.
        Args:
            movies (dict): A dictionary where each key is a movie title, and each
                           value is a dictionary of movie details (Year, Rating, Poster).
        """
        pass

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie entry to storage.
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The IMDb rating of the movie.
            poster (str): The URL of the movie's poster image.
        """
        movies = self.list_movies()

        movies[title] = {
            "Year": year,
            "Rating": rating,
            "Poster": poster
        }

        self.save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie entry from storage by title.
        Args:
            title (str): The title of the movie to be deleted.
        """
        movies = self.list_movies()

        if title in movies:
            del movies[title]
            self.save_movies(movies)
        else:
            print(Fore.RED + f"The movie '{title}' was not found.")

    def update_movie(self, title, rating):
        """
        Update the IMDb rating of an existing movie in storage.
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        """
        movies = self.list_movies()

        if title in movies:
            movies[title]["Rating"] = rating
            self.save_movies(movies)
        else:
            print(Fore.RED + f"The movie '{title}' was not found.")