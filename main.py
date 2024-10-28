from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Main function to run the Movie Database application.
    This function initializes the storage system using StorageJson,
    creates an instance of MovieApp with the storage, and starts the app.
    Returns:
        None
    """
    storage = StorageJson('data.json')  # Initialize the storage with a JSON file.
    movie_app = MovieApp(storage)  # Create an instance of MovieApp with the storage.
    movie_app.run()


if __name__ == "__main__":
    main()
