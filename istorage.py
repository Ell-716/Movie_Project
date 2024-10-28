from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """
        Retrieves a list of movies from the storage.
        Returns:
            dict: A dictionary containing movie titles as keys and their details as values.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating):
        """
        Adds a new movie to the storage.
        Args:
            title (str): The title of the movie to be added.
            year (int): The release year of the movie.
            rating (float): The rating of the movie (0-10).
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage.
        Args:
            title (str): The title of the movie to be deleted.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of an existing movie in the storage.
        Args:
            title (str): The title of the movie to be updated.
            rating (float): The new rating of the movie (0-10).
        """
        pass
