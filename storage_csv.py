import csv
import os
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initializes the StorageCsv instance.
        Args:
            file_path (str): The path to the CSV file for storing movie data.
        """
        self._file_path = file_path

    def load_data(self):
        """
        Loads movie data from the CSV file and returns it as a dictionary.
        Returns:
            dict: A dictionary containing movie titles as keys and their details (year and rating) as values.
        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        if not os.path.exists(self._file_path):
            return {}  # Return an empty dictionary if the file does not exist

        movies = {}
        with open(self._file_path, mode="r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:  # Expecting three columns: title, year, and rating
                    title, year, rating = row
                    movies[title] = {'year': int(year), 'rating': float(rating)}
        return movies

    def save_movies(self, movies):
        """
        Saves the movies to the CSV file.
        Args:
            movies (dict): A dictionary of movies to save.
        """
        with open(self._file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for title, details in movies.items():
                writer.writerow([title, details['year'], details['rating']])

    def list_movies(self):
        """
        Returns the dictionary of movies loaded from the CSV file.
        Returns:
            dict: A dictionary of movies with their details.
        """
        return self.load_data()

    def add_movie(self, title, year, rating):
        """
        Adds a new movie to the storage.
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
        """
        movies = self.load_data()
        movies[title] = {'year': year, 'rating': rating}
        self.save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the storage.
        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.load_data()
        if title in movies:
            del movies[title]
            self.save_movies(movies)

    def update_movie(self, title, rating):
        """
        Updates the rating of an existing movie.
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        """
        movies = self.load_data()
        if title in movies:
            movies[title]['rating'] = rating
            self.save_movies(movies)
