from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """
    Main function to run the Movie Database application.
    This function initializes the storage system based on user input,
    creates an instance of MovieApp with the selected storage, and starts the app.
    Returns:
        None
    """
    print("Welcome to the Movie Database!")
    print("Select storage type:")
    print("1. JSON Storage")
    print("2. CSV Storage")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        filename = input("Enter the name of the JSON file (e.g., data.json): ")
        storage = StorageJson(filename)
    elif choice == '2':
        filename = input("Enter the name of the CSV file (e.g., movies.csv): ")
        storage = StorageCsv(filename)
    else:
        print("Invalid choice. Defaulting to JSON Storage with 'data.json'.")
        storage = StorageJson('data.json')

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
