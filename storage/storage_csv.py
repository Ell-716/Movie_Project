import csv
import os
from storage.istorage import IStorage


class StorageCsv(IStorage):
    """
    A storage handler class for managing movie data in a CSV file format.
    This class provides methods for loading, saving, and managing movie data, stored
    in a structured format where each row corresponds to a movie, and columns include
    the title, year, rating, poster, and flags.
    Attributes:
        file_path (str): The path to the CSV file where movie data is stored.
    Methods:
        list_movies():
            Retrieves a dictionary of movies loaded from the CSV file,
            where each movie title is a unique key and its value is a dictionary
            containing details such as Year, Rating, Poster, and Flags.
        save_movies(movies):
            Saves the current state of the movies to the CSV file, writing
            a header row followed by each movie's details as a new row in the file.
    """

    def __init__(self, file_path):
        """
        Initializes the StorageCsv instance.
        Args:
            file_path (str): The path to the CSV file for storing movie data.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Retrieves a dictionary of movies loaded from the CSV file.
        Returns:
            dict: A dictionary of movies with their details.
        """
        if not os.path.exists(self.file_path):
            return {}

        movies = {}
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if isinstance(row, dict) and all(k in row for k in
                                                 ['Title', 'Year', 'Rating', 'Poster', 'imdbID', 'Flag']):
                    title = row['Title']
                    try:
                        year = int(row['Year'])
                        rating = float(row['Rating']) if row['Rating'] else None
                        poster = row['Poster']
                        note = row.get('Note', '')
                        imdb_link = row['imdbID']
                        flag_urls = row['Flag'].split(",") if row['Flag'] else []

                        movies[title] = {
                            "Year": year,
                            "Rating": rating,
                            "Poster": poster,
                            "Note": note,
                            "imdbID": imdb_link,
                            "Flag": flag_urls
                        }
                    except ValueError as ve:
                        print(f"Error converting data for movie '{title}': {ve}")
                        continue
        return movies

    def save_movies(self, movies):
        """Saves the current state of the movies to the CSV file.
        Args:
            movies (dict): A dictionary of movies containing their details.
        """
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Year', 'Rating', 'Poster', 'Note', 'imdbID', 'Flag'])

            writer.writeheader()

            for title, details in movies.items():
                flag_str = ",".join(details['Flag']) if details.get('Flag') else ''
                writer.writerow({
                    "Title": title,
                    "Year": details['Year'],
                    "Rating": details['Rating'],
                    "Poster": details['Poster'],
                    "Note": details.get('Note', ''),
                    "imdbID": details.get('imdbID', ''),
                    "Flag": flag_str
                })
