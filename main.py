from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp
import os


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
        filename = input("Enter the name of the JSON file (without extension, e.g., data): ")
        if not filename.endswith('.json'):
            filename += '.json'  # Ensure it ends with .json
        filepath = os.path.join('data', filename)  # Construct the full path
        storage = StorageJson(filepath)
    elif choice == '2':
        filename = input("Enter the name of the CSV file (without extension, e.g., movies): ")
        if not filename.endswith('.csv'):
            filename += '.csv'  # Ensure it ends with .csv
        filepath = os.path.join('data', filename)  # Construct the full path
        storage = StorageCsv(filepath)
    else:
        print("Invalid choice. Defaulting to JSON Storage with 'data.json'.")
        storage = StorageJson('data/data.json')  # Ensure correct default path

    try:
        movie_app = MovieApp(storage)
        movie_app.run()
    except Exception as e:
        print(f"An error occurred while running the application: {e}")


if __name__ == "__main__":
    main()
