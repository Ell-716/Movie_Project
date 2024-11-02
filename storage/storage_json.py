import json
from storage.istorage import IStorage


class StorageJson(IStorage):
    """
    A storage handler class for managing movie data in a JSON file format.
    This class provides methods for loading, saving, and managing movie data, stored
    as a dictionary of dictionaries structure, where each movie title is a unique key,
    and its value is a dictionary of details (Year, Rating, Poster etc.).
    Attributes:
        file_path (str): The path to the JSON file where movie data is stored.
    Methods:
        list_movies():
            Reads the JSON file and returns a dictionary of movies with their details,
            where the movie title is the key.
        save_movies(movies):
            Writes a dictionary of movies and their details to the JSON file,
            replacing any existing data in the file.
    """

    def __init__(self, file_path):
        """
        Initializes the StorageJson instance.
        Args:
            file_path (str): The path to the JSON file where movie data is stored.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Retrieves the list of movies from the JSON file.
        Returns:
            dict: A dictionary containing movie titles as keys and their details as values.
                  Returns an empty dictionary if the file is missing, contains invalid JSON,
                  or has an unexpected structure.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    print("Invalid data structure in JSON. Expected a dictionary.")
                    return {}
        except FileNotFoundError:
            print("The JSON file does not exist. Returning an empty dictionary.")
            return {}
        except json.JSONDecodeError:
            print("Error: JSON file contains invalid JSON.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    def save_movies(self, movies):
        """
        Saves the current state of movies to the JSON file.
        Args:
            movies (dict): A dictionary where each key is a movie title, and each value is a dictionary
                           of movie details including 'Year', 'Rating', 'Poster' etc.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(movies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"An error occurred while saving the movies: {e}")
