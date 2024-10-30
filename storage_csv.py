import csv
import os
from istorage import IStorage


class StorageCsv(IStorage):
    """StorageCsv class implements the IStorage interface for managing movie data in CSV format."""

    def __init__(self, file_path):
        """
        Initializes the StorageCsv instance.
        Args:
            file_path (str): The path to the CSV file for storing movie data.
        """
        self._file_path = file_path

    def list_movies(self):
        """
        Retrieves a dictionary of movies loaded from the CSV file.
        Returns:
            dict: A dictionary of movies with their details.
        """
        if not os.path.exists(self._file_path):
            return {}

        movies = {}
        with open(self._file_path, mode="r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure all expected keys are present in the row
                if isinstance(row, dict) and all(k in row for k in ['Title', 'Year', 'Rating', 'Poster']):
                    title = row['Title']
                    try:
                        # Convert year to int and rating to float
                        year = int(row['Year'])
                        rating = float(row['Rating']) if row['Rating'] else None
                        poster = row['Poster']

                        # Store movie details in the correct format
                        movies[title] = {
                            "Year": year,
                            "Rating": rating,
                            "Poster": poster
                        }
                    except ValueError as ve:
                        print(f"Error converting data for movie '{title}': {ve}")
                        continue  # Skip this movie entry if conversion fails

        return movies

    def save_movies(self, movies):
        """Saves the current state of the movies to the CSV file.
        Args:
            movies (dict): A dictionary of movies containing their details.
        """
        with open(self._file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Year", "Rating", "Poster"])

            # Write the header row
            writer.writeheader()

            # Write each movie's details
            for title, details in movies.items():
                writer.writerow({
                    "Title": title,
                    "Year": details["Year"],
                    "Rating": details["Rating"],
                    "Poster": details["Poster"]
                })
