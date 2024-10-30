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
        if not filename.endswith('.json'):
            print("Invalid filename. Defaulting to 'data.json'.")
            filename = 'data.json'
        storage = StorageJson(filename)
    elif choice == '2':
        filename = input("Enter the name of the CSV file (e.g., movies.csv): ")
        if not filename.endswith('.csv'):
            print("Invalid filename. Defaulting to 'movies.csv'.")
            filename = 'movies.csv'
        storage = StorageCsv(filename)
    else:
        print("Invalid choice. Defaulting to JSON Storage with 'data.json'.")
        storage = StorageJson('data.json')

    try:
        movie_app = MovieApp(storage)
        movie_app.run()
    except Exception as e:
        print(f"An error occurred while running the application: {e}")


if __name__ == "__main__":
    main()
