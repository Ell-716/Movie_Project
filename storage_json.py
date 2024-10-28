from istorage import IStorage
import json


class StorageJson(IStorage):
    """StorageJson class implements IStorage interface for managing movie data in JSON format."""

    def __init__(self, file_path):
        """
        Initialize the StorageJson instance.
        Args:
            file_path (str): The path to the JSON file where movie data is stored.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Retrieve the list of movies from the JSON file.
        Returns:
            dict: A dictionary containing movie titles and their details if successful,
                  or an empty dictionary if an error occurs.
        """
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    print("Invalid data structure in JSON. Expected a dictionary.")
                    return {}
        except FileNotFoundError:
            print("The data.json file does not exist. Returning an empty dictionary.")
            return {}
        except json.JSONDecodeError:
            print("Error: data.json contains invalid JSON.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    def save_movies(self, movies):
        """
        Save the movie data to the JSON file.
        Args:
            movies (dict): A dictionary containing movie titles and their details.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump(movies, file)
        except Exception as e:
            print(f"An error occurred while saving the movies: {e}")

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the JSON file.
        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL or path of the movie's poster.
        """
        movies = self.list_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self.save_movies(movies)

    def delete_movie(self, title):
        """
        Delete a movie from the JSON file by title.
        Args:
            title (str): The title of the movie to be deleted.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self.save_movies(movies)
        else:
            print(f"The movie {title} was not found.")

    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie.
        Args:
            title (str): The title of the movie to be updated.
            rating (float): The new rating for the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self.save_movies(movies)
        else:
            print(f"The movie {title} was not found.")
