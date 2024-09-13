import json

def get_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    The function loads the information from the JSON file and returns the data.
    Validates if the file exists, checks if the file contains valid JSON,
    and ensures the structure is a dictionary of dictionaries.
    """
    try:
        with open("data.json", "r") as file:
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


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    try:
        with open("data.json", "w") as file:
            json.dump(movies, file)
        return
    except Exception as e:
        print(f"An error occurred while saving the movies: {e}")


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    del movies[title]
    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title]["rating"] = rating
    save_movies(movies)
